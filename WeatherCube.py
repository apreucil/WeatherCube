#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 14:37:43 2022

@author: anthonypreucil
"""
# Weather Cube Program

# About
# Note: GitHub update will take place outside of this program.

#%% Import Libraries
import pandas as pd
import numpy as np
import re
import geocoder
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (12,7)
# import cartopy
import geopy.distance as gd
import requests
from colormap import hex2rgb, rgb2hex
import pigpio
import os
import wwa
import sched, time
import fading
from connectivity import *

def turn_off():
    pi.set_PWM_dutycycle(17,0)
    pi.set_PWM_dutycycle(22,0)
    pi.set_PWM_dutycycle(24,0)

# FIX THIS
# Idea - write a bash script to do this instead, then call the bash.
# Or - make the bash scipt part of the startup script
# os.system('sudo pigpiod')
pi = pigpio.pi()

# #%% wait for wifi connectivity before running
# # Assume connection problems
# connected = is_connected()
# while not connected:
#     list_of_wifi = get_wifi_networks()
#     if network != None:
#         not_connected == False
#     else:
#         pass

#%% Get curernt Location of Device and Locations of Stations

zipcode = "62644"
test_loc = True
myloc = geocoder.ip('me')
if myloc.latlng == None or test_loc==True:
    # Back up by using zip code
    # Tests
    import pgeocode as pg
    nomi = pg.Nominatim('US')
    print(nomi.query_postal_code(zipcode))
    myloc = pd.DataFrame()
    myloc['latlng'] = [nomi.query_postal_code(zipcode).latitude,nomi.query_postal_code(zipcode).longitude]
# print(myloc.latlng)

stations = pd.read_excel(r'/home/admin/WeatherCube/NWS_Stations.xlsx',index_col='STID')
stations['DistanceToMe'] = [gd.distance((myloc.latlng[0],myloc.latlng[1]),(lat,lon)).km for (lat, lon) in zip(stations.Latitude, stations.Longitude)]
stations.sort_values(by='DistanceToMe',inplace=True)
#%% Generate Color List

temp_rgbs = [(90,0,140),
             (135,0,140),
             (180,0,140),
             (255,0,140),
             (0,0,255),
             (17,223,140),
             (0,255,70),
             (0,255,0),
             (255,180,0),
             (255,80,0),
             (255,30,0),
             (255,15,0),
             (255,0,0)]
    
cm = ListedColormap([tuple([t/255 for t in c]) for c in temp_rgbs], 'wcube', N=13)
#%% Temperature Pattern DataFrame Set up
pattern = pd.DataFrame(index = np.arange(-15,115,10))

pattern['temp_color'] = temp_rgbs
pattern[['r','g','b']] = pattern['temp_color'].tolist()

pattern_df = pd.DataFrame(index=np.arange(-50,150))
pattern_df = pattern_df.join(pattern).drop('temp_color',axis=1)
pattern_df.iloc[0] = [90,0,140]
pattern_df.iloc[-1] = [255,0,0]
pattern_df.interpolate(inplace=True)
pattern_df = pattern_df.round(0).astype(int)

temp_color_key = pd.DataFrame(index=pattern_df.index)
temp_color_key['temp_color'] = list(zip(pattern_df.r,pattern_df.g,pattern_df.b))

#%% Get current temperature
t_re = r'Temperature:<\/span><\/td><td>\s*(-?\d*\.\d*)'

s = sched.scheduler(time.time, time.sleep)

def get_temp_color():
    data = False
    i=1
    while data == False:
        try:
            location = stations.head(i).index[i-1]
            #Note - try this: https://www.weather.gov/wrh/timeseries?site=KVAY
            r = requests.get(r'https://www.aviationweather.gov/metar/data?ids='+location+'&format=decoded&hours=0&taf=off&layout=on')
            html = r.text
            current_temp_F = round(float(re.findall(t_re,html)[0])*9/5+32,0)
            data = True
        except:
            i+=1
            
    # print ('Current Temperature at '+location+': '+str(current_temp_F))
    
    ### Generate current temperature color 
    return temp_color_key.temp_color[temp_color_key.index == int(current_temp_F)].values[0]


def set_color(sc,myloc):
    # print ('setting color')
    global current_temp_color
    current_temp_color = get_temp_color()

    r,g,b = (current_temp_color)
    #set red RGB:
    pi.set_PWM_dutycycle(17,r)
    #set green RGB:
    pi.set_PWM_dutycycle(22,g)
    #set blue RGB:
    pi.set_PWM_dutycycle(24,b)

    # Wait 5 minutes before updating the color.
    sc.enter(300, 1, set_color, (sc,myloc))
    
def check_alert(sc,myloc):
    global alert
    try:
        alert = wwa.get_alerts(myloc,test=False)
    except Exception as e:
        alert = None
        print ('An error occured when trying to get the WWA status. The error was:\n')
        print (e)
    # r,g,b = get_temp_color()
    
    sc.enter(60,1,check_alert,(sc,myloc))
def run_fade(sc,):
    r,g,b = current_temp_color
    if alert==1:
        fading.flash(1)
    elif alert==2:
        fading.reset(r,g,b)
        fading.flash(2)
    elif alert==3:
        fading.fade(40,3)
    elif alert==4:
        fading.reset(r,g,b)
        fading.fade(40,4)
    elif alert==5:
        fading.reset(r,g,b)
        fading.fade(40,5)
    elif alert==None:
        fading.reset(r,g,b)
    else:
        pass
    sc.enter(4,1,run_fade,(sc,))

#%% Run the schedules
alert = None # default
current_temp_color = (250,250,250) # default

# Run the set color program first, then check for update every 5 minutes.
s.enter(1, 1, set_color, (s,myloc))

# Check for alert, then check every 60 seconds
s.enter(1, 1, check_alert, (s,myloc))

# Use value of alert to trigger fading, if neccesary
s.enter(1, 1, run_fade, (s,))

# Finally, run the schedules
s.run()
# Nothing can happen after this line

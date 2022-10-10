#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 14:37:43 2022

@author: anthonypreucil
"""
# Weather Cube Program

# About


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

def turn_off():
    pi.set_PWM_dutycycle(17,0)
    pi.set_PWM_dutycycle(22,0)
    pi.set_PWM_dutycycle(24,0)

# FIX THIS
# os.system('sudo pigpiod')
pi = pigpio.pi()
#%% Get curernt Location of Device and Locations of Stations

myloc = geocoder.ip('me')
print(myloc.latlng)

stations = pd.read_excel(r'NWS_Stations.xlsx',index_col='STID')
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
# FIX THIS!!!
# temp_hexes = [rgb2hex(t[0],t[1],t[2]) for t in temp_rgbs]
        
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

from time import time, sleep
while True:
    sleep(300 - time() % 300) # Runs the code every 5 minutes when
    # time is divisble by 5 (e.g. 9:00, 9:05, 9:10, etc.)
    #print ('Running...')
    location = stations.head(1).index[0]
    r = requests.get(r'https://www.aviationweather.gov/metar/data?ids='+location+'&format=decoded&hours=0&taf=off&layout=on')
    html = r.text
    
    current_temp_F = round(float(re.findall(t_re,html)[0])*9/5+32,0)
    #print ('Current Temperature at '+location+': '+str(current_temp_F))
    
    ### Generate current temperature color 
    current_temp_color = temp_color_key.temp_color[temp_color_key.index == int(current_temp_F)].values[0]
    # Test Display Color
    '''
    plt.figure(figsize=(5,5))
    plt.scatter(1,1,color=rgb2hex(current_temp_color[0],
                                  current_temp_color[1],
                                  current_temp_color[2]),s=5000)
    plt.text(1,1,current_temp_F)
    plt.show()
    '''
    
    r,g,b = (current_temp_color)
    
#     print (r,g,b)
    #set red RGB:
    pi.set_PWM_dutycycle(17,r)
    #set green RGB:
    pi.set_PWM_dutycycle(22,g)
    #set blue RGB:
    pi.set_PWM_dutycycle(24,b)
    '''
    cont = input('Do you wish to continue? [y/n]: ')
    if cont =='n':
        turn_off()
        break 
    else:
        pass
    '''
    
    


















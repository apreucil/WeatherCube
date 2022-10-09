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

stations = pd.read_excel(r'/home/admin/Desktop/NWS_Stations.xlsx',index_col='STID')
stations['DistanceToMe'] = [gd.distance((myloc.latlng[0],myloc.latlng[1]),(lat,lon)).km for (lat, lon) in zip(stations.Latitude, stations.Longitude)]
stations.sort_values(by='DistanceToMe',inplace=True)
'''
#%% Test Location
fig = plt.subplot(projection=cartopy.crs.PlateCarree())

plt.scatter(stations.Longitude,stations.Latitude,color='b',s=10)
plt.scatter(myloc.latlng[1],myloc.latlng[0],color='r')
for s in range(0,5):
    plt.plot([myloc.latlng[1],stations.iloc[s].Longitude],[myloc.latlng[0],stations.iloc[s].Latitude],label='station: '+stations.index[s])
plt.gca().add_feature(cartopy.feature.COASTLINE)
plt.gca().add_feature(cartopy.feature.STATES)
# plt.xlim(-140,-40)
# plt.ylim(20,80)
plt.legend()
plt.xlim(-76,-74)
plt.ylim(39.5,40.5)
plt.show()
'''
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
temp_hexes = [rgb2hex(t[0],t[1],t[2]) for t in temp_rgbs]
cm = ListedColormap(temp_hexes, 'wcube', N=13)

#%% Temperature Pattern DataFrame Set up
pattern = pd.DataFrame(index = np.arange(-20,110))

temp_pattern = [[x]*10 for x in temp_hexes]
temp_pattern_flat = [t for temp in temp_pattern for t in temp]

pattern['temp_color'] = temp_pattern_flat

pattern_extend = pd.DataFrame(index=[-50,150],
                              data={'temp_color':['#502F7D','#520F0B']})

pattern_fill = pd.DataFrame(index=[x for x in range(121,150)],columns=['temp_color'])
pattern_fillLow = pd.DataFrame(index=[x for x in range(-50,-20)],columns=['temp_color'])

temp_color_key = pattern.append(pattern_extend).append(pattern_fill).append(pattern_fillLow).sort_index()
temp_color_key.fillna(method='bfill',inplace=True)


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
    plt.scatter(1,1,color=current_temp_color,s=5000)
    plt.text(1,1,current_temp_F)
    plt.show()
    '''
    
    r,g,b = hex2rgb(current_temp_color)
    
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
    
    


















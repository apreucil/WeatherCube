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
import cartopy
import geopy.distance as gd
import requests
from colormap import hex2rgb

#%% Get curernt Location of Device and Locations of Stations

myloc = geocoder.ip('me')
print(myloc.latlng)

stations = pd.read_excel(r'/Users/anthonypreucil/WeatherCubeProject/NWS_Stations.xlsx',index_col='STID')
stations['DistanceToMe'] = [gd.distance((myloc.latlng[0],myloc.latlng[1]),(lat,lon)).km for (lat, lon) in zip(stations.Latitude, stations.Longitude)]
stations.sort_values(by='DistanceToMe',inplace=True)

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

#%% Generate Color List

temp_hexes = ['#502F7D',
              '#9647D6',
              '#B300FF',
              '#E600FF',
              '#2513ED',
              '#13DFED',
              '#00FFB3',
              '#0A7A50',
              '#C8ED4C',
              '#E6AE15',
              '#F24A41',
              '#990D06',
              '#520F0B']


temp_rgbs = [hex2rgb(h) for h in temp_hexes]

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
    sleep(60 - time() % 60)
	# thing to run
    print ('Running...')
    location = stations.head(1).index[0]
    r = requests.get(r'https://www.aviationweather.gov/metar/data?ids='+location+'&format=decoded&hours=0&taf=off&layout=on')
    html = r.text
    
    current_temp_F = round(float(re.findall(t_re,html)[0])*9/5+32,0)
    print ('Current Temperature: '+str(current_temp_F))
    
    ### Generate current temperature color 
    current_temp_color = temp_color_key.temp_color[temp_color_key.index == int(current_temp_F)].values[0]
    
    # Test Display Color
    plt.figure(figsize=(5,5))
    plt.scatter(1,1,color=current_temp_color,s=5000)
    plt.text(1,1,current_temp_F)
    plt.show()


















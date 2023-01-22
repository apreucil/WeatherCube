#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 14:21:21 2022

@author: anthonypreucil
"""
# Check for Advisory, Watch, Warning for location

import json
import requests
import pandas as pd
import geocoder

def get_alerts(lat,lon,test=False):
    myloc = geocoder.ip('me')
    lat,lon = myloc.latlng[0],myloc.latlng[1]
    
    alert_json = json.loads(requests.get(r'https://api.weather.gov/alerts/active?point='+str(lat)+','+str(lon)).text)
    

    test_json = json.loads(requests.get(r'https://api.weather.gov/alerts/active?point=37.26,-104.33').text)
    if test == True:
        alert_json = test_json
    else:
        pass
    
    
    alerts = []
    for alert in alert_json['features']:
        alerts.append(alert['properties']['event'])
        
    current_alerts = pd.DataFrame(alerts,columns=['CurrentAlerts'])
        
    # get all possible alerts
    alert_list = pd.read_html(requests.get(r"https://www.weather.gov/help-map").content)[0]
    
    alerts_df = pd.merge(current_alerts,alert_list,left_on='CurrentAlerts',right_on='Hazard / Weather Event  Click on the Hazard/Weather Event For Definitions')
    alerts_df.sort_values(by='Priority',inplace=True)
    alerts_df.reset_index(inplace=True,drop=True)
    
    # Special Warnings get special colors, others get slow fade in and out
    if alerts_df.Priority.min() <= 2:
        # print ('Tornado/Tsunami: Flash Red/White')
        return 1
    elif 'Severe Thunderstorm Warning' in alerts_df.CurrentAlerts.values:
        # print ('Severe T-Storm: Flash ?Yellow?')
        return 2
    elif 'Blizzard Warning' in alerts_df.CurrentAlerts.values:
        # print ('Blizzard Warning: Slow fade purple to red')
        return 3
    elif any(i in alerts_df.CurrentAlerts.values for i in ['Flash Flood Warning','Flash Flood Statement']):
        # print ('Flash Flood: Flash Green')
        return 4
    elif alerts_df.Priority.min() <= 120:
        # print ('Hazard in effect: Slow fade of current color')
        return 5
    else:
        # print ('No Hazards')
        return None
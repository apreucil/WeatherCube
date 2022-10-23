#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 16:02:08 2022

@author: anthonypreucil
"""
# test scheduler
import requests
import sched, time
import re

s = sched.scheduler(time.time, time.sleep)
def do_something(sc): 
    print("Doing stuff...")
    # do your stuff
    sc.enter(1, 1, do_something, (sc,))

def do_something_else(sc): 
    t_re = r'Temperature:<\/span><\/td><td>\s*(-?\d*\.\d*)'
    location = 'KVAY'
    r = requests.get(r'https://www.aviationweather.gov/metar/data?ids='+location+'&format=decoded&hours=0&taf=off&layout=on')
    html = r.text
    # Note - try this: https://www.weather.gov/wrh/timeseries?site=KVAY
    current_temp_F = round(float(re.findall(t_re,html)[0])*9/5+32,0)
    print ('Current Temperature at '+location+': '+str(current_temp_F))

    # getting the timing
    sc.enter(5, 1, do_something_else, (sc,))
    
s.enter(1, 1, do_something_else, (s,))    
s.enter(1, 1, do_something, (s,))

s.run()
    
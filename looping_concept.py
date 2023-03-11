#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 15:29:30 2023

@author: anthonypreucil
"""
# Proof of concepts for loops

import wwa
import geocoder
import sched
import time
import pandas as pd
import threading


s = sched.scheduler(time.time, time.sleep)


def set_color(sc, myloc):

    
    fid_temp = open('test2.txt','r')
    temp = fid_temp.read()
    fid_temp.close()
    
    print('setting color ######################################## ' + temp)

    # alert = check_alert(myloc)
    # print (alert, ' : Is the current alert')
    # Wait 5 minutes before updating the code.
    sc.enter(30, 1, set_color, (sc, myloc))


def check_alert(sc, myloc):
    global alert
    print('Checking alert')
    start = time.time()

    try:
        alert = wwa.get_alerts(myloc, test=False)
        # fid = open('test.txt','r')
        # alert = int(fid.read())
        # fid.close()
        print ('alert is '+str(alert))
    except Exception as e:
        alert = None
        print('An error occured when trying to get the WWA status. The error was:\n')
        print(e)

    sc.enter(5, 1, check_alert, (sc, myloc))
    
def run_fade(sc,):
    if alert==1:
        print ('alert'+str(alert))
    elif alert==2:
        print ('alert'+str(alert))
    elif alert==3:
        print ('alert'+str(alert))
    elif alert==4:
        print ('alert'+str(alert))
    elif alert==5:
        print ('alert'+str(alert))
    elif alert==None:
        print ('alert'+str(alert))
    else:
        print ('no alerts :)')
    # time.sleep(2)
    sc.enter(1,1,run_fade, (sc,))


myloc = geocoder.ip('me')
test_loc = True
zipcode = '93643'
if myloc.latlng == None or test_loc == True:
    # Back up by using zip code
    # Tests
    import pgeocode as pg
    nomi = pg.Nominatim('US')
    print(nomi.query_postal_code(zipcode))
    myloc = pd.DataFrame()
    myloc['latlng'] = [nomi.query_postal_code(
        zipcode).latitude, nomi.query_postal_code(zipcode).longitude]
# print(myloc.latlng)

alert = None
s.enter(1, 1, set_color, (s, myloc))
s.enter(1, 1, check_alert, (s, myloc))
s.enter(1, 1, run_fade, (s,))
s.run()

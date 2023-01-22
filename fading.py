#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 16:46:40 2022

@author: anthonypreucil
"""

# This the code to fade the cube based on the watch/warning/advisroy status

import pigpio
import time
import pandas as pd
import numpy as np

# uncomment for pi
pi = pigpio.pi()
# interp_df

def fade(speed, alert_num=5):
    # Save original values
    global rr
    global gg
    global bb
    rr,gg,bb = tuple([pi.get_PWM_dutycycle(i) for i in [17,22,24]])

    # uncomment for mac
    # r,g,b = (200,56,90)
    if alert_num==3:
        # Blizzard Warning Slow fade red to purple
        r,g,b = (255,0,0)
        er,eg,eb = (50,0,255)
    elif alert_num ==4:
        r,g,b = (rr,gg,bb)
        er,eg,eb = (0,255,0)
        # Flash Flood or Flood, slow fade to green and back
    elif alert_num ==5:
        # Any other alert, slow fade of current color
        r,g,b = (rr,gg,bb)
        er,eg,eb = (r/4,g/4,b/4)
    else:
        pass
    
    df = pd.DataFrame([r,g,b]).transpose()
    blank = pd.DataFrame(index=np.arange(speed))
    df = pd.concat([df,blank]).reset_index(drop=True)
    df.loc[speed] = [er,eg,eb] # dip to brightness or other color

    interp_df = df.interpolate()
    interp_df = pd.concat([interp_df,interp_df[::-1]]).round().astype(int).reset_index(drop=True)
    x = 0

    fade=True
    while fade:
        #print (x)
        pi.set_PWM_dutycycle(17,interp_df[0][x])
        pi.set_PWM_dutycycle(22,interp_df[1][x])
        pi.set_PWM_dutycycle(24,interp_df[2][x])
        if x < len(interp_df)-1:
            x+=1
        else:
            fade=False
        # delay
        time.sleep(0.05)
        
def reset(rr,gg,bb):
        pi.set_PWM_dutycycle(17,rr)
        pi.set_PWM_dutycycle(22,gg)
        pi.set_PWM_dutycycle(24,bb)

def flash(alert_num):
    if alert_num == 1:
        # Tornado/Tsunami Flash Red White
        pi.set_PWM_dutycycle(17,255)
        pi.set_PWM_dutycycle(22,0)
        pi.set_PWM_dutycycle(24,0)
        time.sleep(1)
        pi.set_PWM_dutycycle(17,255)
        pi.set_PWM_dutycycle(22,255)
        pi.set_PWM_dutycycle(24,255)
        time.sleep(1)
        pi.set_PWM_dutycycle(17,255)
        pi.set_PWM_dutycycle(22,0)
        pi.set_PWM_dutycycle(24,0)
        time.sleep(1)
        pi.set_PWM_dutycycle(17,255)
        pi.set_PWM_dutycycle(22,255)
        pi.set_PWM_dutycycle(24,255)
        time.sleep(1)
    elif alert_num == 2:
        # Severe Thunderstorm Warning Flash Yellow
        rr,gg,bb = tuple([pi.get_PWM_dutycycle(i) for i in [17,22,24]])
        pi.set_PWM_dutycycle(17,255)
        pi.set_PWM_dutycycle(22,180)
        pi.set_PWM_dutycycle(24,0)
        time.sleep(1)
        reset(rr,gg,bb)
        time.sleep(1)
        pi.set_PWM_dutycycle(17,255)
        pi.set_PWM_dutycycle(22,180)
        pi.set_PWM_dutycycle(24,0)
        time.sleep(1)
        reset(rr,gg,bb)
        time.sleep(1)
    else:
        pass
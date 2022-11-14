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

def fade(speed):
    # Save original values
    global rr
    global gg
    global bb
    rr,gg,bb = tuple([pi.get_PWM_dutycycle(i) for i in [17,22,24]])
    
    # set values for fading
    r,g,b = tuple([pi.get_PWM_dutycycle(i) for i in [17,22,24]])

    # uncomment for mac
    # r,g,b = (200,56,90)
    df = pd.DataFrame([r,g,b]).transpose()
    blank = pd.DataFrame(index=np.arange(speed))
    df = pd.concat([df,blank]).reset_index(drop=True)
    df.at[speed,:] = [r/4,g/4,b/4] # dip to quarter brightness

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
        
def reset():
        pi.set_PWM_dutycycle(17,rr)
        pi.set_PWM_dutycycle(22,gg)
        pi.set_PWM_dutycycle(24,bb)

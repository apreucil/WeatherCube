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
r,g,b = tuple([pi.get_PWM_dutycycle(i) for i in [17,22,24]])

# uncomment for mac
# r,g,b = (200,56,90)

speed = 20

df = pd.DataFrame([r,g,b]).transpose()
blank = pd.DataFrame(index=np.arange(speed))
df = df.append(blank).reset_index(drop=True)
df.at[speed,:] = [r/2,g/2,b/2] # dip to half brightness

interp_df = df.interpolate()
interp_df = interp_df.append(interp_df[::-1]).round().astype(int)
# interp_df

def fade():
    x = 0
    fade=True
    while fade:
        pi.set_PWM_dutycycle(17,interp_df[0][x])
        pi.set_PWM_dutycycle(22,interp_df[1][x])
        pi.set_PWM_dutycycle(24,interp_df[2][x])
        x+=1
        if x >=len(interp_df):
            x==0
        else:
            fade=False
        # delay
        time.sleep(0.05)
        
        
        
    
    
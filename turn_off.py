#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 20:44:39 2022

@author: anthonypreucil
"""

# Script to turn off the WeatherTube

#%% Import Libraries

import pigpio
pi = pigpio.pi()

def turn_off():
    pi.set_PWM_dutycycle(17,0)
    pi.set_PWM_dutycycle(22,0)
    pi.set_PWM_dutycycle(24,0)
    
    
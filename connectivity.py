#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 13:43:39 2022

@author: anthonypreucil
"""
import socket
import subprocess
import re

def is_connected():
    try:
        # connect to the host -- tells us if the host is actually reachable
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False

def get_wifi_networks():
    networks = []
    try:
        output = subprocess.run(["iwlist", "scan"], capture_output=True).stdout.decode("utf-8")
        lines = output.split("\n")
        for line in lines:
            if "ESSID" in line:
                network_name = line.split(":")[1].replace('"', "")
                networks.append(network_name)
    except Exception as e:
        print(e)
    return networks

def get_known_networks():
    fid = open("/etc/wpa_supplicant/wpa_supplicant.conf")
    lines = fid.readlines()
    nets = [re.findall(r'\tssid="(.*)"',l) for l in lines]
    known_networks = [n[0] for n in nets if n!=[]]
    return known_networks
    
def check_connected():
    res_hot_spot = False
    web_server = False
    while not is_connected():
        if res_hot_spot == False:
            # Case to deal with the broken autohotspot
            print ('What wifi is avail?')
            wifi_list = get_wifi_networks()
            known_networks = get_known_networks()
            check = all(item in known_networks for item in wifi_list)
            if check:
                # This means we have a network saved that is available,
                # but the pi is not connected. This is due to two possible
                # issues.
                # 1 - The autohotspot has failed to recognize the available
                # netowork and has started to broadcast its own wifi
                # 2 - The user has changed the wifi password
                # Solution: Try to restart the autohotspot, then recheck
                # the connectivity.
                print ('restart the autohotspot')
                os.chdir('/home/admin')
                os.system('sudo systemctl restart autohotspot')
                res_auto_hotspot=True
                
            else:
                # This is the case where there are no known networks
                # which means the user has changed the SSID or the weather
                # cube is out of range of the signal.
                print ('user needs to set up wifi')
                # Start the web server
                
        elif res_hot_spot == True:
            # This is the case where the we have determined there is a known
            # wifi network in range, but reseting the hotspot failed to connect
            # most likely due to an incorrect user password.
            print ('User wifi password is incorrect')
            # start web server
            
    # we have broken out of the while loop which means we are now connected to
    # the internet. We can now safely start the weather cube program.
    print ('Starting pullcheck for weather tube')
    
check_connected()

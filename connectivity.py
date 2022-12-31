#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 13:43:39 2022

@author: anthonypreucil
"""
import socket
import subprocess

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

# Example usage
print ('Connected To Internet: '+is_connected())
networks = get_wifi_networks()
print(networks)

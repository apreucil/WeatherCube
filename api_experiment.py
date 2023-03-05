#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 19:17:21 2023

@author: anthonypreucil
"""
# Scrape webpage
import requests
import pandas as pd

# url = 'https://www.weather.gov/wrh/timeseries?site=KVAY'
url = r'https://api.mesowest.net/v2/stations/timeseries?STID=KVAY&showemptystations=1&units=temp|F,speed|mph,english&recent=60&token=d8c6aee36a994f90857925cea26934be&complete=1&obtimezone=local'

response = requests.get(url)

json = response.json()

df = pd.DataFrame.from_dict(json['STATION'][0]['OBSERVATIONS'])

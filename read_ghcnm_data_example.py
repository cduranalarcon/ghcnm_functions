#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 16:20:05 2021

@author:Claudio Duran-Alarcon
"""
# Script to select and read ghcnm date by area and station code.

import matplotlib.pyplot as plt
from ghcnm_functions import *

#User parameters
data_fname          = "ghcnm.tavg.v4.0.1.20210818.qcu.dat"
metadata_fname      = "ghcnm.tavg.v4.0.1.20210818.qcu.inv"
selected_stns_fname = 'ghcnm_selected_stations.csv'
path_out            = "data/"

### Retrieve stations
## Select by station code OR area
stations = select_stations(area = [-63,-62,-60,-58], #[lat0, lon0, lat1, lon1]
                           output_fname = selected_stns_fname,
                           data_fname=data_fname,
                           metadata_fname = metadata_fname,
                           ) # station_code = ["AFM00040990","AGE00135039"], # Additional options for selecting stations by CODE

#######FIGURE
fig = plt.figure(figsize=[15,8])

for stn in stations.index:
    df = read_date(path_out+stations.code[stn]+'.csv')
    plt.plot(df,label = stations.name[stn])
plt.xlabel('Time',fontsize=20)
plt.ylabel('Temperature [°C]',fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.legend(fontsize=10)
plt.show()        

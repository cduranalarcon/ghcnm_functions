#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 19 17:40:13 2021

@author:Claudio Duran-Alarcon
"""
# Script to select and read ghcnm date by area and station code.


def select_stations(station_code   = None, 
                    area           = [-90,-180,-60,180], 
                    metadata_fname = "ghcnm.tavg.v4.0.1.20210818.qcu.inv",
                    data_fname     = "ghcnm.tavg.v4.0.1.20210818.qcu.data",
                    output_fname   = 'ghcnm_selected_stations.csv'):

    import pandas as pd

    txt = open(metadata_fname)
    stns = txt.readlines()

    code = []
    latitude = []
    longitude = []
    elevation = []
    name = []

    for s in stns:
        line = s.split()
        if station_code == None:
            lat = float(line[1])
            lon = float(line[2])
            if (lat >= area[0]) & (lat <= area[2]) & (lon >= area[1]) & (lon <= area[3]):     
                code.append(line[0])
                latitude.append(lat)
                longitude.append(lon)
                elevation.append(line[3])
                name.append(line[4])
        else:
            stn_code = line[0]
            if stn_code in station_code:
                code.append(stn_code)
                latitude.append(float(line[1]))
                longitude.append(float(line[2]))
                elevation.append(line[3])
                name.append(line[4])                

    dic = {'code'      : code,
           'latitude'  : latitude,
           'elevation' : elevation,
           'name'      : name,
          }

    stations = pd.DataFrame(dic)

    stations.to_csv(output_fname,index = False)
    
    get_stations(output_fname)
    
    return(stations)
    
def get_stations(selected_stns_fname,
                 data_fname = "ghcnm.tavg.v4.0.1.20210818.qcu.dat",
                 path_out   = "data/"):

    import pandas as pd
    import numpy as np
    import os

    if os.path.exists(path_out) == False: os.mkdir(path_out)
        
    stations = pd.read_csv(selected_stns_fname)

    txt = open(data_fname)
    lines = txt.readlines()
    station_codes = np.array([l[:11] for l in lines])

    for stn in range(np.size(stations['code'])):
        
        fname_out = path_out+stations['code'][stn]+'.csv'
        
        if os.path.isfile(fname_out) == False:
        
            pix = np.squeeze(np.where(station_codes == stations['code'][stn]))

            nyears = np.size(pix)
            date = []
            T = []
            for l in np.array(lines)[pix]:
                for m in range(12):
                    date.append(l[11:15]+'-'+str(m+1).zfill(2))

                    T.append(float(l[19+(m)*8:19+5+(m)*8])) 
            T = np.array(T)  
            T = np.ma.masked_where(T == -9999, T)/100.

            dic = {'date' : date,
                   'T'    : T}

            data = pd.DataFrame(dic)

            data.to_csv(fname_out,index = False)    
    
def read_date(fname):
    import pandas as pd

    df = pd.read_csv(fname, index_col=[0])
    df.index = pd.to_datetime(df.index, format="%Y-%m")
    
    return(df)
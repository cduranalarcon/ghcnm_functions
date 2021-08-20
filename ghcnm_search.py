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
                    output_list    = 'ghcnm_selected_stations.csv',
                    output_path    =  "/data"):

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

    stations.to_csv(output_list,index = False)
    
    get_stations(output_list,data_fname = data_fname, path_out = output_path)
    
    return(stations)
    
def get_stations(selected_stns_fname,
                 data_fname = "ghcnm.tavg.v4.0.1.20210818.qcu.dat",
                 path_out   = "data/"):
    
    #print(selected_stns_fname,data_fname,path_out)

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


import argparse, os
import numpy as np

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tool to select and read ghcnm datasets by area OR station code")
    parser.add_argument("-d","--data_path", type=str, help="Filepath to ghcnm data (ghcnm.tavg.vn.y.z.YYYMMDD.qcu.dat)", required=True)
    parser.add_argument("-m","--metadata_path", type=str, help="Filepath to ghcnm metadata (ghcnm.tavg.vn.y.z.YYYMMDD.qcu.inv)", required=True)
    parser.add_argument("-o","--output_path", type=str, help="Output filepath", default = 'ghcnm_out/')
    parser.add_argument("-s","--stations_list", type=str, help="Name of the stations selected by area or a list of station code",default = 'stations.csv')
    parser.add_argument("-c","--codes", type=str, nargs='+', help="List of station codes within the ghcnm dataset [code1 code2 code3 code4 ...]. When --codes is provides, --area is not used.")
    parser.add_argument("-a","--area", type=float, nargs='+', help="Geographic coordinates of the opposite vertices of a rectangle [minlat minlon maxlat maxlon]", default = [9999,9999,9999,9999])
    args = parser.parse_args()

    missing_args = False

    if (9999 in args.area) and (args.codes == None): 
        print( ' ')
        parser.error('No action requested, add --area or --codes')
        missing_args = True

    if missing_args == False:
        ### Retrieve stations
        ## Selected by station code OR area

        data_path_abs = os.path.abspath(os.path.normpath(args.data_path))
        metadata_path_abs = os.path.abspath(os.path.normpath(args.metadata_path))

        if os.path.exists(os.path.normpath(args.output_path)) == False: os.mkdir(os.path.normpath(args.output_path))
        if os.path.exists(os.path.normpath(args.output_path) +  '/stations/') == False: os.mkdir(os.path.normpath(args.output_path) +  '/stations/')
        if os.path.exists(os.path.normpath(args.output_path) +  '/stations/') == False: os.mkdir(os.path.normpath(args.output_path) +  '/data/')

        os.chdir(os.path.normpath(args.output_path))


        stations = select_stations(
                                   station_code   = args.codes, 
                                   area           = args.area, 
                                   output_list    = 'stations/'  + args.stations_list,
                                   data_fname     = data_path_abs,
                                   metadata_fname = metadata_path_abs,
                                   output_path    = 'data/',
                                   ) 
        print("###############################################################")
        print(" ")
        if np.size(stations.code) == 1:
            print(np.size(stations.code), "station was found.")
        else:
            print(np.size(stations.code), "stations were found.")
        if np.size(stations.code) > 0:
            print(" ")
            print(stations)
            print(" ")
            print("Output files were saved in ","'" + os.path.abspath(os.getcwd())+ "'")
        print(" ")
        print("###############################################################")

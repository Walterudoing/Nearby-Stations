# -*- coding: utf-8 -*-
# Finding the nearby stations according to a given geo-cordinates
# March 25st, 2016
# Walter Lin

import glob
import pandas as pd
import numpy as np
from math import *

#prompt
target_geoco = raw_input('Enter the geo-cordinates, for example 39.8922422,116.3172457 --->   ') 
target_lat = float(target_geoco.split(',')[0])
target_lon = float(target_geoco.split(',')[1])

#path to directory
filepath = '/Users/Walter/Projects/python/nearbyStations/data'

all_files = glob.glob(filepath + "/*.csv")

# Construct an empty DataFrame
frame = pd.DataFrame()

# Construct an empty list
list_ = []

for f in all_files:

	#  encoding="gb2312" 中文不乱码
    df = pd.read_csv(f, header = 1, engine = 'c', sep = ';', names = ['stationNumber', 'stationName', 'province', 'latitude', 'longitude','levitation'], encoding="gb2312")

    # Put all the df into list
    list_.append(df)

# Put the list into frame as our new DataFrame
frame = pd.concat(list_)

# Change all string in 'latitude' and 'stationNumber' columns into int
frame.latitude = frame.latitude.astype(np.int)
frame.stationNumber = frame.stationNumber.astype(np.int)

# Function that turn the values into decimal degree
def decimalDegree(d):
	return float(int(d/100) + float(d)%100/60)

# Create new column for decimal latitude
frame['new_latitude'] = frame.apply(
	lambda row: decimalDegree(row['latitude']),
	axis = 1
)

# Create new column for decimal longitude
frame['new_longitude'] = frame.apply(
	lambda row: decimalDegree(row['longitude']),
	axis = 1
)

# Remove Duplicated items in DataFrame
frame.drop_duplicates('stationNumber', inplace = True)

# Haversine function to calculate the station distance
def haversine_distance(tlon,tlat,lon,lat):

	# Earth radius in km
	R = 6371
	
	# convert decimal degrees to radians 
	tlon = radians(tlon)
	tlat = radians(tlat)
	lon = radians(lon)
	lat = radians(lat)

	# haversine formula 
	dlon = lon - tlon 
	dlat = lat - tlat 
	a = pow(sin(dlat/2),2) + cos(tlat) * cos(lat) * pow(sin(dlon/2),2)
	c = 2 * atan2(sqrt(a),sqrt(1-a))

	return R * c

# Create new column for the distances
frame['h_distance'] = frame.apply(
	lambda row: haversine_distance(target_lat,target_lon,row['new_latitude'],row['new_longitude']),
	axis = 1
)

# sort distance in order to output the shortest distance
frame = frame.sort_values(['h_distance','stationNumber'] , ascending = [True, False])

# output first ten stations
print frame.head(10)
# print frame

# save to file
frame.head(10).to_csv('result.csv', sep = '\t', encoding = 'utf-8', index = False)
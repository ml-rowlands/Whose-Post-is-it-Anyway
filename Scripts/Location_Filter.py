#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 14:48:41 2023

@author: Erika
"""

# function to filter activities by location
# could make object oriented by having the data set be the object and 
# .location_filter(lat, lon) be a method
# could add capability for user to enter city, state type location
# rather than lat, lon type

import pandas as pd
import dfply# dplyr-like package for python

def location_filter(data, start_lat, start_lon, rad, units = "miles"):
    """ filter data to activities starting near start_lat, start_lon
        
        Keyword arguments:
           data -- (pandas DataFrame) the dataset to filter, type StravaData
           start_lat -- (num) the latitude to filter near
           start_lon -- (num) the longitude to filter near
           rad -- (num) the radius of the filter region
           units -- (str) default "miles". The units of rad. Alt = "kilometers"
           
        Returns:
            (pandas DataFrame) a filtered dataset of only activies within rad
            of start_lat, start_lon
    """
    
    # convert units to miles
    if units == "kilometers":
        rad = 0.621371*rad
    # convert radius distance to coordinate distance (this will be challenging
    # as distance corresponding to one decimal longitude changes with latitude)
    rad_lat = 1# make into the proper decimal distances as function of rad, start_lat
    rad_lon = 1
    # filter dataset
    data = data >> dfply.mask(dfply.X.start_latlng[0] < start_lat + rad_lat,
                              dfply.X.start_latlng[0] > start_lat - rad_lat,
                              dfply.X.start_latlng[1] < start_lon + rad_lon,
                              dfply.X.start_latlon[1] > start_lon - rad_lon)
    # return filtered dataset
    return data
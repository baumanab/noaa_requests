#!/usr/bin/env python
# coding: utf-8


"""Python code for querying NOAA daily summary weather and returnig a CSV per year
for a specfic station.  Code is intended to be executed from CLI."""

import sys

# set path to tools library and import
sys.path.append(r'noaa_weather_tools')
from noaa_weather_tools import noaa_weather_tools


print("Check dt format('YYYY-MM-DD', and whether dates span <= 1 year from a current or past date")
print("If dates exceed one year, NCDC query returns a null object.\n")
print("Need a token take a token, have a token, keep it to yourself @ https://www.ncdc.noaa.gov/cdo-web/token\n")
print('start_dt: {}\nend_dt: {}'.format(sys.argv[1], sys.argv[2]))
print('Station: {}\n'.format(sys.argv[3]))


def noaa_dailysum_weather_processor(start_dt, end_dt, station):

    """Function accepts a station ID, and beginning/end datetime as strings with date format as
    'YYYY-MM-DD' which span <= 1 year from a current or past date, passing them to the query_builder function. 
    Function creates a .csv file of NOAA (NCDC) Daily Summary data for a specific station."""
    
    
    print(15 * '.' + "reticulating splines" + 5* '.' + "getting records\n")    
    df, record_count, query_parameters= noaa_weather_tools.get_ncdc(start_dt, end_dt, station)
    
    
    print(15* '.' + "exporting to csv\n")
    my_csv, my_path= noaa_weather_tools.gen_csv(df, query_parameters)
    
    print('spines reticulated............. filename= {}'.format(my_path))
    return my_csv

noaa_dailysum_weather_processor(sys.argv[1], sys.argv[2], sys.argv[3])


 

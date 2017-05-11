#!/usr/bin/env python
# coding: utf-8

"""Python code for querying NOAA daily summary weather and returnig a CSV per year
for a specfic station.  Code is intended to be executed from CLI."""

import sys

# set path to tools library and import
sys.path.append(r'noaa_weather_tools')
from noaa_weather_tools import noaa_weather_tools

print("Check dt format('YYYYMMDD mm:ss', and whether dates span <= 1 year from a current or past date")
print('start_dt: {}\n end_dt: {}'.format(sys.argv[1], sys.argv[2]))


def noaa_dailysum_weather_processor(start_dt, end_dt):

    """Function accepts a beginning and end datetime string in the form 'YYYYMMDD mm:ss' which span <= 1 year from
    a current or past date, passing them to the query_builder function. Function creates a .csv file
    of NOAA Daily Summary data for a specific station."""

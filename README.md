# NOAA Daily Summary Requests

Set of functions to pull down NCDC daily summary data for one year for a specific
station. Functions can be extended with batch or linux scripts to execute for
stations and years.

- Temperature is returned in Fahrenheit
- [Data Type Documentation](
 https://www1.ncdc.noaa.gov/pub/data/cdo/documentation/GHCND_documentation.pdf)

### How to use

 - Clone or download repo
 - Navigate to noaa_requests folder
 - Obtain an API token here: https://www.ncdc.noaa.gov/cdo-web/token
 - Enter token near begin of noaa_weather_tools.py (instruction in .py)
 - Open a shell or command window (install python if not already installed)
 - Execute via Command Line Interface (CLI)



### Example Use

#### Doc String

Function accepts a station ID, and beginning/end datetime as strings with date format as
'MM-DD-YYYY' which span <= 1 year from a current or past date, passing them to the query_builder function. Function creates a .csv file of NOAA (NCDC) Daily Summary data for a specific station.

#### CLI Execution

```python
python noaa_daily_weather_sum.py '2014-05-03' '2015-05-02' 'GHCND:USW00023174'
```

#### Screen Output

```python
Check dt format('DD-MM-YYYY', and whether dates span <= 1 year from a current or past date
If dates exceed one year, NCDC query returns a null object.

Need a token take a token, have a token, keep it to yourself @ https://www.ncdc.noaa.gov/cdo-web/token.

start_dt: 2014-05-03
end_dt: 2015-05-02
Station: GHCND:USW00023174

...............reticulating splines.....getting records

...............exporting to csv

spines reticulated............. filename= GHCND_USW00023174_2014-05-03_2015-05-02.csv
```

#### Example CSV Output
https://github.com/baumanab/noaa_requests/blob/master/GHCND_USW00023174_2014-05-03_2015-05-02.csv






### TODO
- convert to classes and methods
- add decorator to execute function
- create wrapper to execute on multiple stations and years

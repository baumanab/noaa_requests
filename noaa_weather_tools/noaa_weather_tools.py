#!/usr/bin/env python
# coding: utf-8

def query_builder(start_dt, end_dt, station, offset= 1):

    """Function accepts: a start and end datetime string in the form 'YYYYMMDD mm:ss'
    which are <= 1 year apart, a station ID, and an offset.
    Function assembles a query parameters/arguments dict and returns an API query and the
    query dictionary (query_dict). The relevant base URL is the NCDC endpoint
    'http://www.ncdc.noaa.gov/cdo-web/api/v2/data?'."""

    import urllib

    # API endpoint
    base_url= 'http://www.ncdc.noaa.gov/cdo-web/api/v2/data?'

    # dict of NOAA query parameters/arguments

    query_dict = dict(startdate= start_dt, enddate= end_dt, stationid= station,
                      offset= offset, datasetid= 'GHCND', limit= 1000)

    # encode arguments

    encoded_args = urllib.urlencode(query_dict)

    # query
    query = base_url + encoded_args

    # decode url % (reconvert reserved characters to utf8 string)
    query= urllib.unquote(query)

    # create and return query from base url and encoded arguments
    return query, query_dict


def offsetter(response):

    """
    Function accepts a restful query response (JSON)
    Function returns a dictionary of offsets to pull the entire query set
    where the set is limited to 1000 records per query. Function also
    returns a record count for use in validation.
    """

    # get repeats and repeat range
    import math
    count= response['metadata']['resultset']['count']
    repeats= math.ceil(count/1000.)
    repeat_range= range(int(repeats))

    # get offsets dictionary

    offset= 1
    offsets= [1]
    for item in repeat_range[1:]:
        offset += 1000
        offsets.append(offset)


    # zip up the results and convert to dictionary
    offset_dict= dict(zip(repeat_range[1:], offsets[1:])) # the first call has been done already to get meta

    return offset_dict, count # for quality control


def execute_query(query):

    """
    Function accepts an NOAA query for daily summaries for a specfic location
    and executes the query.
    Function returns a response (JSON)
    """
    url = query
    # replace token with token provided by NOAA.  Enter token as string
    headers = {'token': NOAA_Token_Here} # https://www.ncdc.noaa.gov/cdo-web/token
    response = requests.get(url, headers = headers)
    response = response.json()

    return response


def extract_results(response):

    """
    Function accepts a NOAA query response (JSON) return the results
    key values as well as the number of records (for use in validation).
    """
    data= response['results']
    # for quality control to verify retrieval of all rows
    length= len(data)

    return data, length


def collator(results):

    """
    Functions accepts the results key of an NOAA query response (JSON)
    and returns a tidy data set in PANDAS, where each record is an
    observation about a day.
    """

    df= pd.DataFrame(results)
    df= df.drop(['attributes','station'], axis=1)
    df= df.pivot(index= 'date',columns= 'datatype', values= 'value').reset_index()

    return df


def get_ncdc(start_dt, end_dt, station):

    """
    Function accepts a start date (MM-DD-YYY) an end date (MM-DD-YYYY)
    and a NOAA station ID.  Date limit is 1 year.
    Function returns a tidy dataset in a PANDAS DataFrame where
    each row represents an observation about a day, a record count
    and a query parameters dictionary.
    """


    # count for verifying retrieval of all rows
    record_count= 0
    # initial query
    query, query_dict= query_builder(start_dt, end_dt, station)
    response= execute_query(query)

    #  extract results and count
    results, length= extract_results(response)
    record_count += length

    # get offsets for remaining queries
    off_d, count= offsetter(response)

    # execute remaining queries and operations
    for offset in off_d:
        query, _= query_builder(start_dt, end_dt, station, off_d[offset])
        print(query)
        response= execute_query(query)
        next_results, next_length= extract_results(response)

        record_count += next_length

        # concat results lists
        results += next_results

    assert record_count == count, 'record count != count'

    collated_data= collator(results)

    return collated_data, record_count, query_dict

    

def gen_csv(df, query_dict):
    """
    Arguments: PANDAS DataFrame, a query parameters dictionary
    Returns: A CSV of the df with dropped index and named by dict params
    """

    # extract params
    station= query_dict['stationid']
    start= query_dict['startdate']
    end= query_dict['enddate']

    # using os.path in case of future expansion to other directories
    path= os.path.join(station + '_' + start + '_' + end + '.' + 'csv')

    # remove problem characters (will add more in future)
    exclude_chars= ':'
    path= path.replace(exclude_chars, "_")

    # export to csv

    my_csv= df.to_csv(path, index= False)

    return my_csv, path

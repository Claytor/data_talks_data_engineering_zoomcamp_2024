import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@data_loader
# function to load urls for green taxi data from 2022
def load_data_from_api(*args, **kwargs):
    urls = [
        # 2022_01
        'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2022-01.parquet',
        #2022_02
        'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2022-02.parquet',
        #2022_03
        'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2022-03.parquet',
        #2022_04
        'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2022-04.parquet',
        #2022_05
        'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2022-05.parquet',
        #2022_06
        'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2022-06.parquet',
        #2022_07
        'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2022-07.parquet',
        #2022_08
        'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2022-08.parquet',
        #2022_09
        'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2022-09.parquet',
        #2022_10
        'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2022-10.parquet',
        #2022_11
        'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2022-11.parquet',
        #2022_12
        'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2022-12.parquet'     
    ]
    # for loop to read url, change dtypes, and parse dates
    dataframes = []
    for url in urls:
        df = pd.read_parquet(
            url #,
            #sep = ','
        )
        dataframes.append(df)
    all_data = pd.concat(dataframes, ignore_index = True)
    return all_data

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

# We need to map out the datatypes for pandas when loading .csv   
taxi_dtypes = {
    'VendorID': pd.Int64Dtype(),
    'passenger_count': pd.Int64Dtype(),
    'trip_distance': float,
    'RatecodeID':pd.Int64Dtype(),
    'store_and_fwd_flag':str,
    'PULocationID':pd.Int64Dtype(),
    'DOLocationID':pd.Int64Dtype(),
    'payment_type': pd.Int64Dtype(),
    'fare_amount': float,
    'extra':float,
    'mta_tax':float,
    'tip_amount':float,
    'tolls_amount':float,
    'improvement_surcharge':float,
    'total_amount':float,
    'congestion_surcharge':float
}

# native date parsing (this lets pandas know you are parsing dates and it'll handle it automatically)
parse_dates = ['lpep_pickup_datetime', 'lpep_dropoff_datetime']   

@data_loader
# function to load urls for green taxi data in Q4 of 2020
def load_data_from_api(*args, **kwargs):
    urls = [
        'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-10.csv.gz',
        'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-11.csv.gz',
        'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-12.csv.gz'
    
    ]
    # for loop to read url, change dtypes, and parse dates
    dataframes = []
    for url in urls:
        df = pd.read_csv(
            url,
            sep = ',',
            compression = 'gzip',
            dtype = taxi_dtypes,
            parse_dates=parse_dates
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
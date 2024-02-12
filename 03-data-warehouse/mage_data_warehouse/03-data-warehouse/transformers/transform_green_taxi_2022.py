import re
import pandas as pd
def camel_to_snake(name):
    """
    Convert a CamelCase name into snake_case.
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

@transformer
def transform(data, *args, **kwargs):
    # Convert column names from CamelCase to snake_case
    data.columns = [camel_to_snake(column) for column in data.columns]
    
    # Convert datetime fields to the right precision (seconds)
    datetime_columns = ['lpep_pickup_datetime', 'lpep_dropoff_datetime']
    for col in datetime_columns:
        if pd.api.types.is_integer_dtype(data[col]) or pd.api.types.is_float_dtype(data[col]):
            # Convert from UNIX epoch time in nanoseconds to datetime
            data[col] = pd.to_datetime(data[col] / 1e9, unit='s')
        elif pd.api.types.is_datetime64_any_dtype(data[col]):
            # Convert to the right precision (seconds)
            data[col] = data[col].dt.floor('S')

    # Convert integer fields to nullable integers
    integer_columns = ['vendor_id', 'passenger_count', 'ratecode_id', 'pu_location_id', 'do_location_id', 'payment_type']
    for col in integer_columns:
        if col in data.columns:
            data[col] = data[col].astype(pd.Int64Dtype())

    # For FLOAT fields
    float_columns = ['trip_distance', 'fare_amount', 'extra', 'mta_tax', 'tip_amount', 'tolls_amount', 'improvement_surcharge', 'total_amount', 'congestion_surcharge']
    for column in float_columns:
        data[column] = data[column].astype(float)

    # For BOOLEAN fields, assuming store_and_fwd_flag is 'Y'/'N'
    data['store_and_fwd_flag'] = data['store_and_fwd_flag'].map({'Y': True, 'N': False}).astype('boolean')
    
    print(data.info())
    return data
    

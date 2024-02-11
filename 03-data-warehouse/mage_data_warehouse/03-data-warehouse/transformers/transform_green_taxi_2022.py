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

    # For INTEGER fields
    integer_columns = ['vendor_id', 'passenger_count', 'ratecode_id', 'PULocationID', 'DOLocationID', 'payment_type']
    for column in integer_columns:
        data[column] = data[column].astype(pd.Int64Dtype())
    
    print(data.info())
    return data
    

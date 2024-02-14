import re
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

    # Counting rows with specific conditions
    null_vendor_id_count = data['vendor_id'].isnull().sum()
    zeros_passenger_count = data[data['passenger_count'] == 0].shape[0]
    zeros_trip_distance_count = data[data['trip_distance'] == 0].shape[0]

    print(f'rides where vendor is null: {null_vendor_id_count}')
    print(f'rides with zero passengers: {zeros_passenger_count}')
    print(f'rides with zero trip distance: {zeros_trip_distance_count}')

    # Creating date columns for pickup and dropoff dates
    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date
    data['lpep_dropoff_date'] = data['lpep_dropoff_datetime'].dt.date

    # Filtering out rows with undesirable conditions
    filtered_data = data[
        (data['passenger_count'] > 0) &
        (data['trip_distance'] > 0) &
        data['vendor_id'].notnull()
    ]
    
    # Get unique vendors
    unique_vendors = filtered_data['vendor_id'].unique()
    print(f'Unique vendors: {unique_vendors}')
    return filtered_data

@test
def test_output(output, *args) -> None:
    null_vendor_id_count = output['vendor_id'].isnull().sum()
    zero_passenger_count = output[output['passenger_count'] == 0].shape[0]
    zero_trip_distance = output[output['trip_distance'] == 0].shape[0]
    assert null_vendor_id_count == 0, "There are rides with null vendor_id 🚕"
    assert zero_passenger_count == 0, 'There are rides with zero passengers 🚖'
    assert zero_trip_distance == 0, 'There are rides with zero trip distance 🛣️'
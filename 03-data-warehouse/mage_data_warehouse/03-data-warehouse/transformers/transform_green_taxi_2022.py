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
    zeros_fare_amount_count = data[data['fare_amount'] == 0].shape[0]

    # assert null_vendor_id_count == 0, "There are rides with null vendor_id 🚕"
    print(f'🚕 rides where vendor is null: {null_vendor_id_count}')
    print(f'🚖 rides with zero passengers: {zeros_passenger_count}')
    print(f'🛣️ rides with zero trip distance: {zeros_trip_distance_count}')
    print(f'💲 rides with zero fare amount: {zeros_fare_amount_count}')
    return data
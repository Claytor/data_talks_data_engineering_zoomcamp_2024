if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@transformer
def transform(data, *args, **kwargs):
    # counting of rows with null VendorID
    null_vendor_id_count = data['VendorID'].isnull().sum()
    # counting of rows with zero passengers
    zeros_passenger_count = data[data['passenger_count'] == 0].shape[0]
    # counting of rows with zero trip distance
    zeros_trip_distance_count = data[data['trip_distance'] == 0].shape[0]

    print(f'rides where vendor is null: {null_vendor_id_count}')
    print(f'rides with zero passengers: {zeros_passenger_count}')
    print(f'rides with zero trip distance: {zeros_trip_distance_count}')
    #renaming columns to camel_case
    data.columns = (data.columns
                    .str.replace(' ', '_')
                    .str.lower()
    )
    # converting making date columns for pickup and drop off dates
    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date
    data['lpep_dropoff_date'] = data['lpep_dropoff_datetime'].dt.date
    # Filtering out rows with zero count or distance and ensuring VendorID is not null
    filtered_data = data[
        (data['passenger_count'] > 0) & 
        (data['trip_distance'] > 0) & 
        data['vendorid'].notnull()
        ]

    return filtered_data

@test
def test_output(output, *args) -> None:
    # Making a test to confirm that there are rides with zero passengers
    null_vendor_id_count = output['vendorid'].isnull().sum()
    zero_passenger_count = output[output['passenger_count'] == 0].shape[0]
    zero_trip_distance = output[output['trip_distance'] == 0].shape[0]
    assert null_vendor_id_count == 0, "There are rides with null vendorid 🚕"
    assert zero_passenger_count == 0, 'There are rides with zero passengers 🚖'
    assert zero_trip_distance == 0, 'There are rides with zero trip distance 🛣️'
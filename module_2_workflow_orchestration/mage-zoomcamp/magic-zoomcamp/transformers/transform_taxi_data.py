if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@transformer
def transform(data, *args, **kwargs):
    """
    Looking for the count of cases where there are zero passengers
    """
    print("Rows with zero passengers 🚖:", data['passenger_count'].isin([0]).sum())
    
    """
    Returning the data with the zero passenger count removed
    """
    return data[data['passenger_count'] > 0]


@test
def test_output(output, *args) -> None:
    """
    Making a test to confirm that there are rides with zero passengers
    """
    assert output['passenger_count'].isin([0]).sum() == 0, 'There are rides with zero passengers 🚖'
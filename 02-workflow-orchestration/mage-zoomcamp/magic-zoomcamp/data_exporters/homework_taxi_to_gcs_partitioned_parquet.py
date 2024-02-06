import pyarrow as pa
import pyarrow.parquet as pq
import os


if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/src/claytor-mage.json"
bucket_name = 'claytor-mage'
project_id = 'Claytor DE Bootcamp'
table_name = 'green_taxi'
root_path = f'{bucket_name}/{table_name}'

@data_exporter
def export_data(data, *args, **kwargs):
    # gives us the date as as string that pyarrow can use
  data['lpep_pickup_date']
    # reads data into a pyarrow table with pandas
  table = pa.Table.from_pandas(data)
    # find google cloud storage object which is in the pyarrow file system.  Authroizes using environment variable automatically
  gcs = pa.fs.GcsFileSystem()
  # Use parquet write to data set method to dataset.  This requires three arguents
  pq.write_to_dataset(
    #first argument is "table" which is a pyarrow table
    table,
    # second argument is "root_path"
    root_path=root_path,
    # third argument is a list "partition_cols" where the columns to partion on are indicated
    partition_cols = ['lpep_pickup_date'],
    # The last argument is the file system, which is the gcs file system
    filesystem=gcs
  )
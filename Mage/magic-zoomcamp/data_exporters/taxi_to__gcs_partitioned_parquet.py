import pyarrow as pa
import pyarrow.parquet as pq
import os


if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/src/claytor-mage.json"

bucket_name = 'claytor-mage'
project_id = 'claytor-mage'

table_name = 'nyc_taxi_data'

root_path = f'{bucket_name}/{table_name}'
@data_exporter
def export_data(data, *args, **kwargs):
    # gives us the date as as string that pyarrow can use
  data['tpep_pickup_date'] = data['tpep_pickup_datetime'].dt.date
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
    partition_cols = ['tpep_pickup_date'],
    # The last argument is the file system, which is the gcs file system
    filesystem=gcs
  )

# This breaks our data up by date and writes to different parquet files. see results in bucket
# this is how larger datasets are managed.  Doesn't make sense to write a 2gb dataset into one file
# it would be really slow to read and write
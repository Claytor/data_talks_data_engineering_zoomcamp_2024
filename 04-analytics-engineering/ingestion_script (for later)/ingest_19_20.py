import io
import os
import requests
import pandas as pd
from google.cloud import storage

# Pre-requisites:
# 1. `pip install pandas pyarrow google-cloud-storage`
# 2. Set GOOGLE_APPLICATION_CREDENTIALS to your project/service-account key
# 3. Set GCP_GCS_BUCKET as your bucket or change default value of BUCKET

# Define the initial URL for downloading the data and the default bucket name.
init_url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/'
BUCKET = os.environ.get("GCP_GCS_BUCKET", "claytor_taxi_warehouse")

def upload_to_gcs(bucket, object_name, local_file):
    """
    Uploads a file to Google Cloud Storage (GCS).
    
    Args:
        bucket (str): The name of the GCS bucket.
        object_name (str): The name/path for the file in the GCS bucket.
        local_file (str): The path to the local file to upload.
    """
    client = storage.Client()
    bucket = client.bucket(bucket)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)

def web_to_gcs(year, service):
    """
    Downloads data for a given year and service, converts it to parquet, and uploads to GCS.
    
    Args:
        year (str): The year of the data to download.
        service (str): The taxi service (e.g., 'green', 'yellow') of the data.
    """
    for i in range(12):  # Loop through all months
        
        # Format the month to ensure it's two digits
        month = '0'+str(i+1)
        month = month[-2:]

        # Construct the file name for the CSV file
        file_name = f"{service}_tripdata_{year}-{month}.csv.gz"

        # Construct the URL and download the file
        request_url = f"{init_url}{service}/{file_name}"
        r = requests.get(request_url)
        open(file_name, 'wb').write(r.content)
        print(f"Local: {file_name}")

        # Read the downloaded CSV file into a DataFrame and convert to Parquet
        df = pd.read_csv(file_name, compression='gzip')
        file_name = file_name.replace('.csv.gz', '.parquet')
        df.to_parquet(file_name, engine='pyarrow')
        print(f"Parquet: {file_name}")

        # Upload the Parquet file to GCS
        upload_to_gcs(BUCKET, f"{service}/{file_name}", file_name)
        print(f"GCS: {service}/{file_name}")

# Example calls to download data for the 'green' service for years 2019 and 2020
web_to_gcs('2019', 'green')
web_to_gcs('2020', 'green')
# The following lines are commented out, but you could uncomment them to download for other years/services
# web_to_gcs('2019', 'yellow')
# web_to_gcs('2020', 'yellow')

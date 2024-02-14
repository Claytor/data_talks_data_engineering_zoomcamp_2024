This code is a Python script designed to automate the process of downloading NYC TLC (Taxi and Limousine Commission) trip data files from a GitHub repository, converting them from CSV to Parquet format, and then uploading them to a Google Cloud Storage (GCS) bucket. It's structured to handle datasets for different taxi services by year and month. Let's break down the functionality step by step:

```mermaid

graph LR;
    A[Start] --> B[Download CSVs from GitHub];
    B --> C[Convert CSV to Parquet];
    C --> D[Upload Parquet to GCS];
    D --> E[End];

```
### Pre-requisites:
- The script requires `pandas`, `pyarrow`, and `google-cloud-storage` Python packages installed. These are essential for data manipulation, file format conversion, and interacting with Google Cloud Storage, respectively.
- It also requires setting up the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to authenticate with Google Cloud using a service account key.
- The `GCP_GCS_BUCKET` environment variable should be set to specify the target Google Cloud Storage bucket. If not set, a default bucket name (`dtc-data-lake-bucketname`) is used.

### Key Components:

#### Global Variables:
- `init_url`: The base URL for downloading the dataset files from GitHub.
- `BUCKET`: The name of the Google Cloud Storage bucket where the files will be uploaded. It tries to read from the environment variable `GCP_GCS_BUCKET` or defaults to `dtc-data-lake-bucketname`.

#### `upload_to_gcs` Function:
- Takes `bucket` (name of the GCS bucket), `object_name` (the GCS object name or path), and `local_file` (the path to the local file to be uploaded).
- It initializes a GCS client, gets the specified bucket, creates a blob object with the given object name, and uploads the file from the given local file path.
- This function encapsulates the GCS upload logic, abstracting away the details of connecting to GCS and handling file uploads.

#### `web_to_gcs` Function:
- Takes `year` and `service` parameters to determine which dataset to process.
- Iterates through all months (1 to 12), constructs the file name for each month's dataset, and downloads the `.csv.gz` file using the `requests` library.
- After downloading, it reads the CSV file into a pandas DataFrame, converts it to Parquet format using the `pyarrow` engine, and saves the Parquet file locally.
- Finally, it uploads the Parquet file to the specified GCS bucket, organizing files by service and maintaining the naming convention.
- This function essentially automates the end-to-end process of acquiring the data, transforming it, and storing it in a cloud-based data lake.

### Execution Calls:
- The script calls `web_to_gcs` function twice, each time specifying a different year (`2019` and `2020`) for the `green` taxi service. 
- It's structured to easily extend or modify to include additional years or services (`fhv`, `green`, `yellow`) by uncommenting the relevant lines.

### Workflow Summary:
1. Download compressed CSV files from a specified URL.
2. Convert each CSV file to Parquet format for more efficient storage and query performance.
3. Upload the Parquet files to a Google Cloud Storage bucket, organizing them by service type and preserving the naming convention for easy retrieval.
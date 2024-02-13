# Week 3 Homework
For this homework I used the 2022 Green Taxi Trip Record Parquet Files from the New York
City Taxi Data found [here](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page).  I used Mage as an orchestrator to load the parquet files into a Google Cloud Storage Bucket.

## Mage Orchestration Pipeline
1) [`load_green_taxi_2022.py`](https://github.com/Claytor/data_talks_data_engineering_zoomcamp_2024/blob/main/03-data-warehouse/mage_data_warehouse/03-data-warehouse/data_loaders/load_green_taxi_2022.py)
2) [`transform_green_taxi_2022.py`](https://github.com/Claytor/data_talks_data_engineering_zoomcamp_2024/blob/main/03-data-warehouse/mage_data_warehouse/03-data-warehouse/transformers/transform_green_taxi_2022.py)
3) [`export_green_taxi_2022`](https://github.com/Claytor/data_talks_data_engineering_zoomcamp_2024/blob/main/03-data-warehouse/mage_data_warehouse/03-data-warehouse/data_exporters/green_taxi_2022_to_gcs.py)
> ![alt text](../images/03_hw_pipeline.png)


## SETUP
### 1) Create an external table using the Green Taxi Trip Records Data for 2022.
```sql 
---------------------------------------------------------------------
-- Creating external table referring to gcs path
---------------------------------------------------------------------
CREATE OR REPLACE EXTERNAL TABLE `zoomcamp-2024.ny_taxi.external_green_2022`
OPTIONS (
  format = 'Parquet',
  uris = ['gs://claytor-mage/green_taxi_2022.parquet']
);
```
### 2) Create a table in BQ using the Green Taxi Trip Records for 2022 
```sql
---------------------------------------------------------------------
-- Create a non-partitioned internalized table from external table. 

-- This may be a bit of tomfoolery. I couldn't get autoschema to recognize the dt columns (unix nanoseconds) so I converted them microseconds and it worked like a charm.  Man this took me forever to figure out. Couldn't get it to work in the pipeline for the life of me!
---------------------------------------------------------------------

CREATE OR REPLACE TABLE zoomcamp-2024.ny_taxi.materialized_green_2022_non_partitioned AS
SELECT
  vendor_id,
  TIMESTAMP_MICROS(DIV(lpep_pickup_datetime, 1000)) AS lpep_pickup_timestamp,
  TIMESTAMP_MICROS(DIV(lpep_dropoff_datetime, 1000)) AS lpep_dropoff_timestamp,
  store_and_fwd_flag,
  ratecode_id,
  pu_location_id,
  do_location_id,
  passenger_count,
  trip_distance,
  fare_amount,
  extra,
  mta_tax,
  tip_amount,
  tolls_amount,
  ehail_fee,
  improvement_surcharge,
  total_amount,
  payment_type,
  trip_type,
  congestion_surcharge
FROM
  zoomcamp-2024.ny_taxi.external_green_2022;
```


## Question 1:
```sql
----------------------------------------------------------------------
--1️⃣) What is count of records for the 2022 Green Taxi Data??
--👉️ 840,402 records
----------------------------------------------------------------------
SELECT
  COUNT(vendor_id)
FROM
  zoomcamp-2024.ny_taxi.external_green_2022;
```

## Question 2:
```sql
----------------------------------------------------------------------
-- 2️⃣) Write a query to count the distinct number of PULocationIDs for 
-- the entire dataset on both the tables.
----------------------------------------------------------------------

--👉️ External Table Estimate: 0b
SELECT 
  DISTINCT(pu_location_id)
FROM
  zoomcamp-2024.ny_taxi.external_green_2022;

--👉️ Internal Table Estimate: 6.41 mb
SELECT 
  DISTINCT(pu_location_id)
FROM 
  zoomcamp-2024.ny_taxi.materialized_green_2022_non_partitioned;
  ```

## Question 3:
```sql
----------------------------------------------------------------------
-- 3️⃣) How many records have a fare_amount of 0?
--👉️ 1,622 records
----------------------------------------------------------------------

SELECT 
  COUNT(fare_amount) AS free_rides
FROM zoomcamp-2024.ny_taxi.external_green_2022
WHERE fare_amount = 0;
```

## Question 4:
```sql
----------------------------------------------------------------------
-- 4️⃣) What is the best strategy to make an optimized table in Big Query if your query will always order the results by PUlocationID and filter based on lpep_pickup_datetime?
--👉️ Partition by lpep_pickup_datetime and cluster by pu_location_id
----------------------------------------------------------------------

CREATE OR REPLACE TABLE
  zoomcamp-2024.ny_taxi.materialized_green_2022_partitioned_clustered
PARTITION BY 
  DATE(lpep_pickup_timestamp)
CLUSTER BY 
  pu_location_id AS
SELECT
  *
FROM
  `zoomcamp-2024.ny_taxi.materialized_green_2022_non_partitioned`;
  ```

## Question 5:
```sql
----------------------------------------------------------------------
--5️⃣) Write a query to retrieve the distinct PULocationID between lpep_pickup_datetime 06/01/2022 and 06/30/2022 (inclusive)
--👉️  Normie Estimates: 12.82 MB
--👉️  Partitioned & Clustered Estimates: 1.12 MB
----------------------------------------------------------------------

-- Only Materialized Estimate: 12.82 MB

SELECT
  DISTINCT(pu_location_id)
FROM 
  zoomcamp-2024.ny_taxi.materialized_green_2022_non_partitioned
WHERE 
  DATE(lpep_pickup_timestamp) 
    BETWEEN '2022-06-01' AND '2022-06-30';

-- Partitioned and Clustered Estimates: 1.12 MB

SELECT
  DISTINCT(pu_location_id)
FROM 
  zoomcamp-2024.ny_taxi.materialized_green_2022_partitioned_clustered
WHERE 
  DATE(lpep_pickup_timestamp) 
    BETWEEN '2022-06-01' AND '2022-06-30';
```


## Question 6: 
Where is the data stored in the External Table you created?

👉️ GCP Bucket



## Question 7:
It is best practice in Big Query to always cluster your data:

👉️ False

It depend on your use case (distribution of values, access frequency, dynamic nature of columns, volume of queries, etc.)


## (Bonus: Not worth points) Question 8:
```sql
----------------------------------------------------------------------
-- BONUS No Points: 
-- Write a SELECT count(*) query FROM the materialized table you created. 
-- How many bytes does it estimate will be read?
-- 👉️ 0 bytes
-- Why?
-- 👉️ I believe that this accesses the view's cached metadata instead of actually querying the table.
----------------------------------------------------------------------

SELECT
  COUNT (*)
FROM
  `zoomcamp-2024.ny_taxi.materialized_green_2022_non_partitioned`
```

 
## Submitting the solutions

* Form for submitting: https://courses.datatalks.club/de-zoomcamp-2024/homework/hw3


---------------------------------------------------------------------
-------------------------- Tables Setup -----------------------------
---------------------------------------------------------------------

---------------------------------------------------------------------
-- Creating external table referring to gcs path
---------------------------------------------------------------------
CREATE OR REPLACE EXTERNAL TABLE `zoomcamp-2024.ny_taxi.external_green_2022`
OPTIONS (
  format = 'Parquet',
  uris = ['gs://claytor-mage/green_taxi_2022.parquet']
);

---------------------------------------------------------------------
-- Create a non-partitioned internalized table from external table
-- Maybe a bit of tomfoolery, but I couldn't get autoschema
-- to recognize the dt columns (unix nano) so I converted them
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

----------------------------------------------------------------------
-- Create a materialized partition table from external table
----------------------------------------------------------------------

CREATE OR REPLACE TABLE `zoomcamp-2024.ny_taxi.materialized_green_2022_partitioned`
PARTITION BY DATE(lpep_dropoff_timestamp) AS
SELECT
  *
FROM
  zoomcamp-2024.ny_taxi.materialized_green_2022_non_partitioned;

----------------------------------------------------------------------
----------------------- HOMEWORK QUESTIONS ---------------------------
----------------------------------------------------------------------

----------------------------------------------------------------------
--1️⃣) What is count of records for the 2022 Green Taxi Data??
--👉️ 840,402 records
----------------------------------------------------------------------
SELECT
  COUNT(vendor_id)
FROM
  zoomcamp-2024.ny_taxi.external_green_2022;
----------------------------------------------------------------------
-- 2️⃣) Write a query to count the distinct number of PULocationIDs for 
-- the entire dataset on both the tables.
----------------------------------------------------------------------

--👉️ External Table Estimate: 0b --
SELECT 
  DISTINCT(pu_location_id)
FROM
  zoomcamp-2024.ny_taxi.external_green_2022;

--👉️ Internal Table Estimate: 6.41 mb --
SELECT 
  DISTINCT(pu_location_id)
FROM 
  zoomcamp-2024.ny_taxi.materialized_green_2022_non_partitioned;

----------------------------------------------------------------------
-- 3️⃣) How many records have a fare_amount of 0?
--👉️ 1622 records
----------------------------------------------------------------------

SELECT 
  COUNT(fare_amount) AS free_rides
FROM zoomcamp-2024.ny_taxi.external_green_2022
WHERE fare_amount = 0;

----------------------------------------------------------------------
-- 4️⃣) What is the best strategy to make an optimized table in Big Query if
------ your query will always order the results by PUlocationID
------ and filter based on lpep_pickup_datetime?
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

----------------------------------------------------------------------
--5️⃣) Write a query to retrieve the distinct PULocationID between
----  lpep_pickup_datetime 06/01/2022 and 06/30/2022 (inclusive)
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

----------------------------------------------------------------------
-- BONUS No Points: 
-- Write a SELECT count(*) query FROM the materialized table you created. 
-- How many bytes does it estimate will be read?
-- 👉️ 0 bytes
-- Why?
-- 👉️ I believe that this accesses the view's cached metadata instead of actually querying the table 
----------------------------------------------------------------------

SELECT
  COUNT (*)
FROM
  `zoomcamp-2024.ny_taxi.materialized_green_2022_non_partitioned`
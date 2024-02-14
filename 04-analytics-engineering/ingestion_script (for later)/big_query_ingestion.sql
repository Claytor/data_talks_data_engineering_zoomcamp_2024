-----------------------------------------------------------------
-- Adding Data To BQ from Public Datasets
-----------------------------------------------------------------
-----------------------------------------------------------------
-----------------------------------------------------------------
-- 1) Creating new tables From BQ from Public Datasets
-----------------------------------------------------------------
--Create table "green_tripdata" into "trips_data_all"
CREATE TABLE  zoomcamp-2024.trips_data_all.green_tripdata as
SELECT * FROM bigquery-public-data.new_york_taxi_trips.tlc_green_trips_2019;

--Create table "yellow_tripdata" into "trips_data_all"
CREATE TABLE  zoomcamp-2024.trips_data_all.yellow_tripdata as
SELECT * FROM bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2019;

-----------------------------------------------------------------
-- 2) Inserting more data into the created tables
-----------------------------------------------------------------
--Insert 2020 data into "green_tripdata" table
INSERT INTO zoomcamp-2024.trips_data_all.green_tripdata
SELECT * FROM bigquery-public-data.new_york_taxi_trips.tlc_green_trips_2020 ;

--Insert 2020 data into "yellow_tripdata" table
INSERT INTO zoomcamp-2024.trips_data_all.yellow_tripdata
SELECT * FROM bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2020 ;
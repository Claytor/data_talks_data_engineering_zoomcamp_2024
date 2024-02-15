
# Module 4: Analytics Engineering

## Setup

### 1) Merging Datasets from public data in Big Query

```mermaid
graph TD
    A([Create a new big query data set 'trips_data_all']) --> B{Create tables from BQ public datasets}
    B --> C[green_tripdata from tlc_green_trips_2019]
    B --> D[yellow_tripdata from tlc_yellow_trips_2019]
    C --> E{Insert more data into tables}
    D --> E
    E --> F[green_tripdata with tlc_green_trips_2020]
    E --> G[yellow_tripdata with tlc_yellow_trips_2020]
```

#### An overview of the data (in millions)

```mermaid
---
config:
    sankey:
         nodeAlignment: 'left'
---
sankey-beta
    trips_data_all: , yellow_trip_2019: ,84.598433
    trips_data_all: , yellow_trip_2020: , 24.649081
    trips_data_all: , green_trip_2019: , 6.300974
    trips_data_all: , green_trip-2020: , 1.734165
```
### 2) Setting up dbt for using BigQuery (cloud)

![alt text](images/image1.png)

Steps

1) create service account
1) give appropriate bq permissions
1) generate key for service account
1) create dbt account
1) make new project
1) set connection to BigQuery
1) upload key for gcp service account
1) setup repository (Git Clone from Personal Repo (ssh))
1) Add deploy key from DBT to GitHub Repo & Allow write access
1) View you Projects in DBT cloud





# Preparing the data for the section 
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
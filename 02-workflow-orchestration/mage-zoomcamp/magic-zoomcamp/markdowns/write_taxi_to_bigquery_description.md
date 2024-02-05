The `transform_staged_data` block returns `df1`

`write_taxi_to_bigquery` exporter uses: 

- BigQuery and default connection
- `ny_taxi` schema
- `yellow_cab_data` table

It selects the transformed data and exports it to the ny_taxy schema.
Go to google bigquery to make sure it got there.
{{
    config(
        materialized='view'
    )
}}

with tripdata as 
(
  select *,
    row_number() over(partition by vendor_id, pickup_datetime) as rn
  from {{ source('staging','green_tripdata') }}
  where vendor_id is not null 
)
select
    -- identifiers
    {{ dbt_utils.generate_surrogate_key(['vendor_id', 'pickup_datetime']) }} as trip_id,
    {{ dbt.safe_cast("vendor_id", api.Column.translate_type("string")) }} as vendor_id,
    SAFE_CAST(SPLIT(rate_code, '.')[SAFE_OFFSET(0)] AS STRING) as rate_code,
    {{ dbt.safe_cast("pickup_location_id", api.Column.translate_type("string")) }} as pickup_location_id,
    {{ dbt.safe_cast("dropoff_location_id", api.Column.translate_type("string")) }} as dropoff_location_id,
    
    -- timestamps
    pickup_datetime,
    dropoff_datetime,
    
    -- trip info
    store_and_fwd_flag,
    passenger_count,
    trip_distance,

    -- payment info
    fare_amount,
    extra,
    mta_tax,
    tip_amount,
    tolls_amount,
    imp_surcharge,
    total_amount,
    {{ dbt.safe_cast("payment_type", api.Column.translate_type("string")) }} as payment_type,
    {{ get_payment_type_description("payment_type") }} as payment_type_description,
    {{ dbt.safe_cast("data_file_year", api.Column.translate_type("string")) }} as data_file_year,
    {{ dbt.safe_cast("data_file_month", api.Column.translate_type("string")) }} as data_file_month

from tripdata
where rn = 1


-- dbt build --select <model_name> --vars '{'is_test_run': 'false'}'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}
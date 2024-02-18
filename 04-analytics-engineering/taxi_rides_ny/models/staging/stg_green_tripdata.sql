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
    {{ dbt.safe_cast("vendor_id", api.Column.translate_type("integer")) }} as vendor_id,
    {{ dbt.safe_cast("rate_code", api.Column.translate_type("integer")) }} as ratecode_id,
    {{ dbt.safe_cast("pickup_location_id", api.Column.translate_type("integer")) }} as pickup_location_id,
    {{ dbt.safe_cast("dropoff_location_id", api.Column.translate_type("integer")) }} as dropoff_location_id,
    
    -- trip info
    store_and_fwd_flag,
    {{ dbt.safe_cast("passenger_count", api.Column.translate_type("integer")) }} as passenger_count,
    cast(trip_distance as numeric) as trip_distance,
    {{ dbt.safe_cast("trip_type", api.Column.translate_type("integer")) }} as trip_type,

    -- payment info
    {{ get_payment_type_description("payment_type") }} as payment_type_description
from tripdata
where rn = 1


-- dbt build --select <model_name> --vars '{'is_test_run': 'false'}'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}
{{ config(materialized='table') }}

with source as (
    -- We point directly to the file using DuckDB's auto-reader
    -- This is very fast and avoids 'Table not found' errors
    select * from read_csv_auto('../data/raw/races.csv')
),

renamed as (
    select
        race_id,
        cast(race_date as date) as race_date,
        upper(venue) as venue_name,
        track_condition,
        cast(prize_money as float) as prize_money_eur,
        cast(loaded_at as timestamp) as inserted_at
    from source
)

select * from renamed
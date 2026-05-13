{{ config(materialized='table') }}

with source as (
    -- We point directly to the file using DuckDB's auto-reader
    -- This is very fast and avoids 'Table not found' errors
    select * from read_csv_auto('../data/raw/races.csv')
),

renamed as (
    SELECT
        {{ dbt_utils.generate_surrogate_key(['race_date', 'num_reunion', 'race_number']) }} as unique_race_key,
        -- Keep the original ID just in case
        race_id as pmu_race_id,
        cast(race_date as date) as race_date,
        venue,
        country,
        weather,
        reunion_nature,
        discipline,
        specialty,
        condition_age,
        cast(prize_money as float) as prize_money,
        cast(runners_count as integer) as runners_count,
        cast(distance as integer) as distance,
        distance_unit,
        is_quinte,
        cast(inserted_at as timestamp) as inserted_at
    FROM source
)

select * from renamed
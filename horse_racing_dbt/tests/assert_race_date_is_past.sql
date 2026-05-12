-- This test catches races with dates in the future
-- (relative to when they were inserted)
select
    race_id,
    race_date,
    inserted_at
from {{ ref('stg_races') }}
where race_date > cast(inserted_at as date)
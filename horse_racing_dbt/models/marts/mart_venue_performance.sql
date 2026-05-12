select
    venue_name,
    count(race_id) as total_races,
    avg(prize_money_eur) as avg_prize,
    max(inserted_at) as last_update
from {{ ref('stg_races') }}
group by 1
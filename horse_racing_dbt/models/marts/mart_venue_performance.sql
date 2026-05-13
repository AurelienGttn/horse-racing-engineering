{{ config(materialized='table') }}

WITH base_races AS (
    SELECT * FROM {{ ref('stg_races') }}
),

venue_metrics AS (
    SELECT
        venue,
        country,
        -- Volume metrics
        COUNT(race_id) as total_races,
        COUNT(DISTINCT race_date) as racing_days,
        
        -- Financial metrics
        ROUND(AVG(prize_money), 0) as avg_prize_pool,
        MAX(prize_money) as record_prize_pool,
        SUM(prize_money) as total_purse_distributed,
        
        -- Competition metrics
        ROUND(AVG(runners_count), 1) as avg_field_size,
        
        -- Weather diversity (how many different conditions recorded)
        COUNT(DISTINCT weather) as weather_variety
        
    FROM base_races
    GROUP BY 1, 2
)

SELECT
    *,
    CASE 
        WHEN avg_prize_pool > 50000 THEN 'Elite'
        WHEN avg_prize_pool > 20000 THEN 'Professional'
        ELSE 'Regional'
    END as venue_tier,
    
    -- Efficiency Metric
    ROUND(total_purse_distributed / NULLIF(total_races, 0), 0) as value_per_race
FROM venue_metrics
WHERE total_races > 1
ORDER BY avg_prize_pool DESC
{{ config(materialized='table') }}

SELECT
    published_date as date,
    mentioned_ticker as ticker,
    COUNT(*) as mention_count,
    COUNT(DISTINCT source_name) as source_count,
    ARRAY_AGG(DISTINCT search_keyword) as keywords
FROM {{ ref('stg_news_articles') }}
WHERE mentioned_ticker IS NOT NULL
GROUP BY published_date, mentioned_ticker
ORDER BY date DESC, mention_count DESC

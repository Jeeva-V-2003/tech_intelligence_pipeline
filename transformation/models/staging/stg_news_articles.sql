{{ config(materialized='view') }}

SELECT
    title,
    description,
    url,
    CAST(publishedAt AS TIMESTAMP) as published_at,
    DATE_TRUNC('day', CAST(publishedAt AS TIMESTAMP)) as published_date,
    source.name as source_name,
    search_keyword,
    CASE
        WHEN LOWER(title) LIKE '%nvidia%' OR LOWER(title) LIKE '%nvda%' THEN 'NVDA'
        WHEN LOWER(title) LIKE '%microsoft%' OR LOWER(title) LIKE '%msft%' THEN 'MSFT'
        WHEN LOWER(title) LIKE '%google%' OR LOWER(title) LIKE '%googl%' THEN 'GOOGL'
        WHEN LOWER(title) LIKE '%meta%' OR LOWER(title) LIKE '%facebook%' THEN 'META'
        WHEN LOWER(title) LIKE '%tesla%' OR LOWER(title) LIKE '%tsla%' THEN 'TSLA'
    END as mentioned_ticker
FROM {{ source('raw_news', 'news_articles') }}
WHERE title IS NOT NULL

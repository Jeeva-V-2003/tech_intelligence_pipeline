{{ config(materialized='view') }}

SELECT
    ticker,
    current_price,
    high,
    low,
    open,
    previous_close,
    CAST(timestamp AS TIMESTAMP) as quote_timestamp,
    DATE_TRUNC('day', CAST(timestamp AS TIMESTAMP)) as quote_date,
    ROUND(((current_price - previous_close) / previous_close) * 100, 2) as price_change_pct
FROM {{ source('raw_finance', 'stock_quotes') }}
WHERE ticker IS NOT NULL

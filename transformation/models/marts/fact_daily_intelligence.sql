{{ config(materialized='table') }}

WITH daily_reddit AS (
    SELECT
        created_date as date,
        COUNT(*) as reddit_post_count,
        AVG(score) as avg_reddit_score,
        AVG(upvote_ratio) as avg_upvote_ratio,
        SUM(CASE WHEN sentiment = 'positive' THEN 1 ELSE 0 END) as positive_posts,
        SUM(CASE WHEN sentiment = 'negative' THEN 1 ELSE 0 END) as negative_posts
    FROM {{ ref('stg_reddit_posts') }}
    GROUP BY created_date
),

daily_news AS (
    SELECT
        published_date as date,
        COUNT(*) as news_article_count,
        COUNT(DISTINCT mentioned_ticker) as tickers_mentioned
    FROM {{ ref('stg_news_articles') }}
    GROUP BY published_date
),

daily_stocks AS (
    SELECT
        quote_date as date,
        ticker,
        AVG(current_price) as avg_price,
        AVG(price_change_pct) as avg_price_change_pct
    FROM {{ ref('stg_stock_quotes') }}
    GROUP BY quote_date, ticker
)

SELECT
    COALESCE(r.date, n.date, s.date) as intelligence_date,
    r.reddit_post_count,
    r.avg_reddit_score,
    r.avg_upvote_ratio,
    r.positive_posts,
    r.negative_posts,
    n.news_article_count,
    n.tickers_mentioned,
    s.ticker,
    s.avg_price,
    s.avg_price_change_pct
FROM daily_reddit r
FULL OUTER JOIN daily_news n ON r.date = n.date
FULL OUTER JOIN daily_stocks s ON COALESCE(r.date, n.date) = s.date
WHERE COALESCE(r.date, n.date, s.date) IS NOT NULL
ORDER BY intelligence_date DESC

{{ config(materialized='view') }}

SELECT
    post_id,
    subreddit,
    title,
    score,
    upvote_ratio,
    num_comments,
    CAST(created_utc AS TIMESTAMP) as created_at,
    DATE_TRUNC('day', CAST(created_utc AS TIMESTAMP)) as created_date,
    CASE
        WHEN upvote_ratio >= 0.8 THEN 'positive'
        WHEN upvote_ratio >= 0.5 THEN 'neutral'
        ELSE 'negative'
    END as sentiment,
    selftext
FROM {{ source('raw_reddit', 'reddit_posts') }}
WHERE post_id IS NOT NULL

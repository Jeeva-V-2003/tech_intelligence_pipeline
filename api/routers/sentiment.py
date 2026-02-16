from fastapi import APIRouter, Query
from api.database import query_to_dict

router = APIRouter()

@router.get("/sentiment")
def get_sentiment(limit: int = Query(30, ge=1, le=365)):
    query = f"""
    SELECT 
        intelligence_date,
        positive_posts,
        negative_posts,
        avg_upvote_ratio,
        ROUND(CAST(positive_posts AS FLOAT) / NULLIF(positive_posts + negative_posts, 0), 2) as sentiment_score
    FROM analytics.fact_daily_intelligence
    WHERE positive_posts IS NOT NULL
    ORDER BY intelligence_date DESC
    LIMIT {limit}
    """
    return query_to_dict(query)

from pydantic import BaseModel
from typing import Optional
from datetime import date

class TrendResponse(BaseModel):
    intelligence_date: date
    reddit_post_count: Optional[int]
    avg_reddit_score: Optional[float]
    news_article_count: Optional[int]
    ticker: Optional[str]
    avg_price: Optional[float]
    avg_price_change_pct: Optional[float]

class SentimentResponse(BaseModel):
    intelligence_date: date
    positive_posts: Optional[int]
    negative_posts: Optional[int]
    avg_upvote_ratio: Optional[float]
    sentiment_score: Optional[float]

class TickerMentionResponse(BaseModel):
    date: date
    ticker: str
    mention_count: int
    source_count: int

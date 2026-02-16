from fastapi import APIRouter, Query
from typing import Optional
from api.database import query_to_dict

router = APIRouter()

@router.get("/trends")
def get_trends(limit: int = Query(30, ge=1, le=365), ticker: Optional[str] = None):
    query = "SELECT * FROM analytics.fact_daily_intelligence"
    if ticker:
        query += f" WHERE ticker = '{ticker}'"
    query += f" ORDER BY intelligence_date DESC LIMIT {limit}"
    return query_to_dict(query)

@router.get("/trends/mentions")
def get_mentions(ticker: Optional[str] = None, limit: int = Query(30, ge=1, le=365)):
    query = "SELECT * FROM analytics.fact_ticker_mentions"
    if ticker:
        query += f" WHERE ticker = '{ticker}'"
    query += f" ORDER BY date DESC LIMIT {limit}"
    return query_to_dict(query)

import dlt
import finnhub
from typing import Iterator, Dict
from datetime import datetime, timedelta
from config import config

@dlt.resource(write_disposition="append")
def stock_quotes() -> Iterator[Dict]:
    """Fetch real-time stock quotes"""
    client = finnhub.Client(api_key=config.FINNHUB_API_KEY)
    
    for ticker in config.STOCK_TICKERS:
        quote = client.quote(ticker)
        yield {
            "ticker": ticker,
            "current_price": quote.get("c"),
            "high": quote.get("h"),
            "low": quote.get("l"),
            "open": quote.get("o"),
            "previous_close": quote.get("pc"),
            "timestamp": datetime.now().isoformat()
        }

@dlt.resource(write_disposition="append")
def company_news() -> Iterator[Dict]:
    """Fetch company-specific news"""
    client = finnhub.Client(api_key=config.FINNHUB_API_KEY)
    today = datetime.now()
    week_ago = today - timedelta(days=7)
    
    for ticker in config.STOCK_TICKERS:
        news = client.company_news(
            ticker,
            _from=week_ago.strftime("%Y-%m-%d"),
            to=today.strftime("%Y-%m-%d")
        )
        for item in news:
            item["ticker"] = ticker
            yield item

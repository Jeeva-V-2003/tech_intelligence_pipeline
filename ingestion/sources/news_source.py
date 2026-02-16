import dlt
import requests
from typing import Iterator, Dict
from config import config

@dlt.resource(write_disposition="append")
def news_articles() -> Iterator[Dict]:
    """Fetch AI and tech news from NewsAPI"""
    for keyword in config.NEWS_KEYWORDS:
        url = f"https://newsapi.org/v2/everything"
        params = {
            "q": keyword,
            "apiKey": config.NEWS_API_KEY,
            "pageSize": 100,
            "sortBy": "publishedAt"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        articles = response.json().get("articles", [])
        for article in articles:
            article["search_keyword"] = keyword
            yield article

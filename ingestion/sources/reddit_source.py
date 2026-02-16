import dlt
import praw
from typing import Iterator, Dict
from datetime import datetime
from config import config

@dlt.resource(write_disposition="append")
def reddit_posts() -> Iterator[Dict]:
    """Fetch posts from tech-related subreddits"""
    reddit = praw.Reddit(
        client_id=config.REDDIT_CLIENT_ID,
        client_secret=config.REDDIT_CLIENT_SECRET,
        user_agent="market_intelligence_bot/1.0"
    )
    
    for subreddit_name in config.SUBREDDITS:
        subreddit = reddit.subreddit(subreddit_name)
        for post in subreddit.hot(limit=100):
            yield {
                "post_id": post.id,
                "subreddit": subreddit_name,
                "title": post.title,
                "score": post.score,
                "upvote_ratio": post.upvote_ratio,
                "num_comments": post.num_comments,
                "created_utc": datetime.fromtimestamp(post.created_utc).isoformat(),
                "url": post.url,
                "selftext": post.selftext[:500] if post.selftext else None
            }

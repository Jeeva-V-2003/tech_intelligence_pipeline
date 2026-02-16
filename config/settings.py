from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    # API Keys
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
    REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
    FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
    
    # Paths
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    WAREHOUSE_DIR = DATA_DIR / "warehouse"
    DUCKDB_PATH = os.getenv("DUCKDB_PATH", str(WAREHOUSE_DIR / "intelligence.duckdb"))
    
    # API Config
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", 8000))
    
    # Data Sources
    SUBREDDITS = ["technology", "wallstreetbets", "artificial"]
    STOCK_TICKERS = ["NVDA", "MSFT", "GOOGL", "META", "TSLA"]
    NEWS_KEYWORDS = ["AI", "Generative AI", "Semiconductors", "OpenAI", "Nvidia"]

config = Config()

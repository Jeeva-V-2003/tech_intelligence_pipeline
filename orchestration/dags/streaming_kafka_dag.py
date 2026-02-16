from airflow.decorators import dag, task
from datetime import datetime, timedelta
import sys
from pathlib import Path

project_root = Path('/opt/airflow/project_root')
sys.path.insert(0, str(project_root))

default_args = {
    "owner": "data_team",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

@dag(
    dag_id="streaming_kafka_pipeline",
    default_args=default_args,
    description="Real-time streaming with Kafka",
    schedule="*/5 * * * *",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["streaming", "kafka", "real-time"],
)
def streaming_kafka_pipeline():
    
    @task
    def stream_news_to_kafka():
        from include.kafka import MarketDataProducer
        from ingestion.sources.news_source import news_articles
        
        producer = MarketDataProducer()
        
        for article in news_articles():
            producer.send_news(article)
        
        producer.flush()
        producer.close()
        return "News streamed to Kafka"
    
    @task
    def stream_reddit_to_kafka():
        from include.kafka import MarketDataProducer
        from ingestion.sources.reddit_source import reddit_posts
        
        producer = MarketDataProducer()
        
        for post in reddit_posts():
            producer.send_reddit(post)
        
        producer.flush()
        producer.close()
        return "Reddit data streamed to Kafka"
    
    @task
    def stream_stocks_to_kafka():
        from include.kafka import MarketDataProducer
        from ingestion.sources.finance_source import stock_quotes
        
        producer = MarketDataProducer()
        
        for quote in stock_quotes():
            producer.send_stock(quote)
        
        producer.flush()
        producer.close()
        return "Stock data streamed to Kafka"
    
    @task
    def consume_and_load_to_duckdb(news_status, reddit_status, stock_status):
        import duckdb
        from include.kafka import MarketDataConsumer
        from config import config
        
        conn = duckdb.connect(config.DUCKDB_PATH)
        
        def process_message(topic, data):
            if topic == 'market-news':
                conn.execute("INSERT INTO raw_news.news_articles SELECT * FROM ?", [data])
            elif topic == 'social-sentiment':
                conn.execute("INSERT INTO raw_reddit.reddit_posts SELECT * FROM ?", [data])
            elif topic == 'stock-prices':
                conn.execute("INSERT INTO raw_finance.stock_quotes SELECT * FROM ?", [data])
        
        consumer = MarketDataConsumer(['market-news', 'social-sentiment', 'stock-prices'])
        
        count = 0
        for message in consumer.consumer:
            process_message(message.topic, message.value)
            count += 1
            if count >= 100:
                break
        
        consumer.close()
        conn.close()
        return f"Consumed {count} messages"
    
    news = stream_news_to_kafka()
    reddit = stream_reddit_to_kafka()
    stocks = stream_stocks_to_kafka()
    
    consume_and_load_to_duckdb(news, reddit, stocks)

dag_instance = streaming_kafka_pipeline()

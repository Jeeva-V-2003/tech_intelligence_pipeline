from kafka import KafkaProducer
import json

class MarketDataProducer:
    def __init__(self, bootstrap_servers='localhost:9092'):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
    
    def send_news(self, news_data):
        self.producer.send('market-news', value=news_data)
    
    def send_reddit(self, reddit_data):
        self.producer.send('social-sentiment', value=reddit_data)
    
    def send_stock(self, stock_data):
        self.producer.send('stock-prices', value=stock_data)
    
    def flush(self):
        self.producer.flush()
    
    def close(self):
        self.producer.close()

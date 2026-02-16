from kafka import KafkaConsumer
import json

class MarketDataConsumer:
    def __init__(self, topics, bootstrap_servers='localhost:9092', group_id='market-intelligence'):
        self.consumer = KafkaConsumer(
            *topics,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest'
        )
    
    def consume(self, callback):
        for message in self.consumer:
            callback(message.topic, message.value)
    
    def close(self):
        self.consumer.close()

#!/usr/bin/env python3
"""Test Kafka producer and consumer"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from orchestration.include.kafka import MarketDataProducer, MarketDataConsumer
import time

def test_producer():
    print("Testing Kafka Producer...")
    producer = MarketDataProducer()
    
    test_data = {
        "title": "Test News Article",
        "source": "Test Source",
        "timestamp": "2026-01-01T00:00:00"
    }
    
    producer.send_news(test_data)
    producer.flush()
    producer.close()
    print("✅ Producer test passed")

def test_consumer():
    print("\nTesting Kafka Consumer...")
    
    def callback(topic, data):
        print(f"Received from {topic}: {data}")
    
    consumer = MarketDataConsumer(['market-news', 'social-sentiment', 'stock-prices'])
    
    print("Listening for 10 seconds...")
    start_time = time.time()
    
    for message in consumer.consumer:
        callback(message.topic, message.value)
        if time.time() - start_time > 10:
            break
    
    consumer.close()
    print("✅ Consumer test passed")

if __name__ == "__main__":
    print("🧪 Kafka Integration Tests\n")
    print("Make sure Kafka is running: docker-compose up -d\n")
    
    try:
        test_producer()
        test_consumer()
        print("\n✅ All tests passed!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)

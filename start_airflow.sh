#!/bin/bash

echo "🚀 AI Market Intelligence Hub - Airflow + Kafka Setup"
echo "======================================================"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo "✅ Docker is running"
echo ""

# Start services
echo "Starting Airflow + Kafka services..."
cd orchestration
docker-compose up -d

echo ""
echo "Waiting for services to be ready..."
sleep 15

echo ""
echo "✅ Setup complete!"
echo ""
echo "📊 Access Points:"
echo "  - Airflow UI: http://localhost:8080 (admin/admin)"
echo "  - Kafka UI: http://localhost:8090"
echo ""
echo "📝 Available DAGs:"
echo "  1. market_intelligence_pipeline (Batch processing)"
echo "  2. streaming_kafka_pipeline (Real-time streaming)"
echo ""
echo "🧪 Test Kafka:"
echo "  make kafka-test"
echo ""
echo "📋 View logs:"
echo "  make logs"
echo ""
echo "🛑 Stop services:"
echo "  make airflow-down"

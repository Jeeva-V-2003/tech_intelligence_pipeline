# Airflow + Kafka Setup Guide

## Quick Start

### 1. Start All Services

```bash
cd orchestration
docker-compose up -d
```

This starts:
- **Airflow Webserver**: http://localhost:8080 (admin/admin)
- **Kafka**: localhost:9092
- **Kafka UI**: http://localhost:8090
- **PostgreSQL**: localhost:5432

### 2. Check Services Status

```bash
docker-compose ps
```

### 3. Access Airflow UI

Open http://localhost:8080
- Username: `admin`
- Password: `admin`

### 4. Access Kafka UI

Open http://localhost:8090 to monitor Kafka topics and messages

## Available DAGs

### 1. market_intelligence_pipeline
- **Schedule**: Hourly
- **Purpose**: Batch ingestion and transformation
- **Steps**:
  1. Ingest Reddit data
  2. Ingest news data
  3. Ingest finance data
  4. Transform with dbt
  5. Run data quality tests

### 2. streaming_kafka_pipeline
- **Schedule**: Every 5 minutes
- **Purpose**: Real-time streaming
- **Steps**:
  1. Stream news to Kafka topic `market-news`
  2. Stream Reddit to Kafka topic `social-sentiment`
  3. Stream stocks to Kafka topic `stock-prices`
  4. Consume and load to DuckDB

## Kafka Topics

- `market-news`: News articles from NewsAPI
- `social-sentiment`: Reddit posts
- `stock-prices`: Real-time stock quotes

## Testing Kafka

### Produce Test Message

```bash
docker exec -it kafka kafka-console-producer \
  --bootstrap-server localhost:9092 \
  --topic market-news
```

### Consume Messages

```bash
docker exec -it kafka kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic market-news \
  --from-beginning
```

### List Topics

```bash
docker exec -it kafka kafka-topics \
  --bootstrap-server localhost:9092 \
  --list
```

## Airflow Commands

### Trigger DAG Manually

```bash
docker exec -it orchestration-airflow-scheduler-1 \
  airflow dags trigger market_intelligence_pipeline
```

### View Logs

```bash
docker-compose logs -f airflow-scheduler
```

### Install Additional Packages

```bash
docker exec -it orchestration-airflow-webserver-1 \
  pip install <package-name>
```

## Stopping Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## Troubleshooting

### Airflow not starting
```bash
# Check logs
docker-compose logs airflow-init

# Restart services
docker-compose restart
```

### Kafka connection issues
```bash
# Check Kafka logs
docker-compose logs kafka

# Verify Kafka is running
docker exec -it kafka kafka-broker-api-versions \
  --bootstrap-server localhost:9092
```

### Permission errors
```bash
# Set correct permissions
export AIRFLOW_UID=$(id -u)
docker-compose down -v
docker-compose up -d
```

## Architecture Flow

```
Data Sources → Kafka Topics → Airflow DAGs → DuckDB → dbt → FastAPI
     ↓              ↓              ↓            ↓       ↓       ↓
  Reddit      social-sentiment  Scheduler   Warehouse Transform API
  NewsAPI     market-news       Tasks       Storage   Models   Endpoints
  Finnhub     stock-prices      Monitoring  Query     Tests    Docs
```

## Monitoring

- **Airflow UI**: Task status, logs, DAG runs
- **Kafka UI**: Topics, messages, consumer groups
- **PostgreSQL**: Airflow metadata

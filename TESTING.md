# Complete Testing Guide

## 🎯 Step-by-Step Testing

### 1. Start Services (Already Running ✅)
```bash
cd orchestration
docker-compose up -d
```

### 2. Test Kafka

#### Check Kafka is running
```bash
docker exec -it kafka kafka-broker-api-versions --bootstrap-server localhost:9092
```

#### Create topics manually
```bash
docker exec -it kafka kafka-topics --create --topic market-news --bootstrap-server localhost:9092
docker exec -it kafka kafka-topics --create --topic social-sentiment --bootstrap-server localhost:9092
docker exec -it kafka kafka-topics --create --topic stock-prices --bootstrap-server localhost:9092
```

#### List topics
```bash
docker exec -it kafka kafka-topics --list --bootstrap-server localhost:9092
```

#### Test producer
```bash
docker exec -it kafka kafka-console-producer --topic market-news --bootstrap-server localhost:9092
# Type a message and press Enter
# Press Ctrl+C to exit
```

#### Test consumer
```bash
docker exec -it kafka kafka-console-consumer --topic market-news --from-beginning --bootstrap-server localhost:9092
```

### 3. Test Airflow

#### Access Airflow UI
Open http://localhost:8080
- Username: `admin`
- Password: `admin`

#### Enable DAGs
1. Find `market_intelligence_pipeline`
2. Toggle the switch to enable it
3. Click the play button to trigger manually

#### View logs
```bash
docker exec -it orchestration-airflow-scheduler-1 airflow dags list
docker exec -it orchestration-airflow-scheduler-1 airflow tasks list market_intelligence_pipeline
```

### 4. Run Data Pipeline

#### Option A: Via Airflow UI
1. Go to http://localhost:8080
2. Click on `market_intelligence_pipeline`
3. Click "Trigger DAG" button
4. Monitor task progress

#### Option B: Via CLI
```bash
docker exec -it orchestration-airflow-scheduler-1 airflow dags trigger market_intelligence_pipeline
```

#### Option C: Run pipelines directly
```bash
# From project root
python -m ingestion.pipelines.news_pipeline
python -m ingestion.pipelines.reddit_pipeline
python -m ingestion.pipelines.finance_pipeline

# Then run dbt
cd transformation
dbt run --profiles-dir .
dbt test --profiles-dir .
```

### 5. Test API

#### Start FastAPI
```bash
cd api
uvicorn main:app --reload --port 8000
```

#### Test endpoints
```bash
# Health check
curl http://localhost:8000/health

# Get trends
curl http://localhost:8000/api/trends

# Get sentiment
curl http://localhost:8000/api/sentiment

# Get ticker mentions
curl http://localhost:8000/api/trends/mentions?ticker=NVDA
```

#### Access Swagger docs
Open http://localhost:8000/docs

### 6. Monitor Kafka UI

Open http://localhost:8090
- View topics
- See message counts
- Monitor consumer groups

## 🧪 Python Test Scripts

### Test Kafka Integration
```bash
python3 tests/test_kafka.py
```

### Test Individual Components
```python
# Test news ingestion
python -m ingestion.pipelines.news_pipeline

# Test Reddit ingestion
python -m ingestion.pipelines.reddit_pipeline

# Test finance ingestion
python -m ingestion.pipelines.finance_pipeline
```

## 📊 Verify Data

### Check DuckDB
```bash
python3 -c "
import duckdb
conn = duckdb.connect('data/warehouse/intelligence.duckdb')
print(conn.execute('SHOW TABLES').fetchall())
conn.close()
"
```

### Query data
```bash
python3 -c "
import duckdb
conn = duckdb.connect('data/warehouse/intelligence.duckdb')
print(conn.execute('SELECT COUNT(*) FROM raw_news.news_articles').fetchone())
conn.close()
"
```

## 🔍 Troubleshooting

### Airflow not accessible
```bash
docker-compose logs airflow-webserver
docker-compose restart airflow-webserver
```

### Kafka connection refused
```bash
docker-compose logs kafka
docker-compose restart kafka
```

### DAG not appearing
```bash
docker exec -it orchestration-airflow-scheduler-1 airflow dags list-import-errors
```

### View container logs
```bash
docker-compose logs -f [service-name]
# Examples:
docker-compose logs -f airflow-scheduler
docker-compose logs -f kafka
```

## 🎉 Success Checklist

- [ ] Airflow UI accessible at http://localhost:8080
- [ ] Kafka UI accessible at http://localhost:8090
- [ ] Kafka topics created and visible
- [ ] DAGs visible in Airflow
- [ ] Pipeline runs successfully
- [ ] Data appears in DuckDB
- [ ] dbt models run successfully
- [ ] API returns data at http://localhost:8000/docs

## 📝 Quick Commands

```bash
# Start everything
make airflow-up

# Test Kafka
make kafka-test

# View logs
make logs

# List Kafka topics
make kafka-topics

# Trigger pipeline
make trigger-dag

# Stop everything
make airflow-down
```

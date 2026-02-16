# Setup Guide

## Prerequisites
- Python 3.9+
- Docker (for Airflow)
- Git

## Quick Start

### 1. Clone and Setup Environment

```bash
cd tech_intelligence_pipeline
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure API Keys

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
- **NewsAPI**: Get from https://newsapi.org/
- **Reddit**: Create app at https://www.reddit.com/prefs/apps
- **Finnhub**: Get from https://finnhub.io/

### 3. Run Data Ingestion (First Time)

```bash
# Ingest Reddit data
python -m ingestion.pipelines.reddit_pipeline

# Ingest news data
python -m ingestion.pipelines.news_pipeline

# Ingest finance data
python -m ingestion.pipelines.finance_pipeline
```

### 4. Transform Data with dbt

```bash
cd transformation
dbt run --profiles-dir .
dbt test --profiles-dir .
cd ..
```

### 5. Start the API

```bash
cd api
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Visit: http://localhost:8000/docs

## Running with Airflow (Optional)

### Setup Airflow with Astro CLI

```bash
# Install Astro CLI
curl -sSL install.astronomer.io | sudo bash -s

# Initialize Airflow
cd orchestration
astro dev init
astro dev start
```

Visit: http://localhost:8080 (user: admin, pass: admin)

## API Endpoints

Once running, access:

- **Swagger Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Daily Trends**: http://localhost:8000/api/trends
- **Sentiment**: http://localhost:8000/api/sentiment
- **Ticker Mentions**: http://localhost:8000/api/trends/mentions?ticker=NVDA

## Project Structure

```
tech_intelligence_pipeline/
├── ingestion/              # dlt data ingestion
│   ├── sources/           # Data source definitions
│   └── pipelines/         # Pipeline runners
├── transformation/         # dbt transformations
│   ├── models/
│   │   ├── staging/      # Cleaned raw data
│   │   └── marts/        # Business logic
│   └── dbt_project.yml
├── orchestration/         # Airflow DAGs
│   └── dags/
├── api/                   # FastAPI application
│   ├── routers/          # API endpoints
│   ├── schemas/          # Pydantic models
│   └── main.py
├── config/               # Configuration
└── data/                 # DuckDB warehouse
```

## Troubleshooting

### DuckDB not found
```bash
mkdir -p data/warehouse
```

### Import errors
```bash
# Run from project root
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### API keys not working
Check `.env` file is in project root and properly formatted.

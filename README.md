# AI Market Intelligence Hub

A modern data pipeline that extracts live crypto/stock data and AI news, transforms it into analytical schemas, and exposes it via FastAPI.

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Sources   │────▶│     dlt     │────▶│   DuckDB    │────▶│     dbt     │
│ Reddit/News │     │  Ingestion  │     │  Warehouse  │     │ Transform   │
│   Finance   │     └─────────────┘     └─────────────┘     └─────────────┘
└─────────────┘                                                      │
                                                                     ▼
┌─────────────┐                                              ┌─────────────┐
│   FastAPI   │◀─────────────────────────────────────────────│  Mart Layer │
│     API     │                                              └─────────────┘
└─────────────┘
```

## Stack

- **Ingestion**: dlt (Data Load Tool)
- **Orchestration**: Apache Airflow
- **Transformation**: dbt (Data Build Tool)
- **Warehouse**: DuckDB
- **API**: FastAPI

## Project Structure

```
tech_intelligence_pipeline/
├── ingestion/          # dlt pipelines
├── transformation/     # dbt models
├── orchestration/      # Airflow DAGs
├── api/               # FastAPI application
├── config/            # Configuration files
└── tests/             # Test suite
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. Initialize dlt:
```bash
cd ingestion
dlt init
```

4. Run Airflow:
```bash
cd orchestration
astro dev start
```

5. Start API:
```bash
cd api
uvicorn main:app --reload
```

## API Endpoints

- `GET /trends` - Daily market intelligence trends
- `GET /sentiment` - Social sentiment analysis
- `GET /health` - API health check

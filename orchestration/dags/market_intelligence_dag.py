from airflow.decorators import dag, task
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

default_args = {
    "owner": "data_team",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

@dag(
    dag_id="market_intelligence_pipeline",
    default_args=default_args,
    description="End-to-end market intelligence data pipeline",
    schedule="@hourly",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["intelligence", "dlt", "dbt"],
)
def market_intelligence_pipeline():
    
    @task
    def ingest_reddit_data():
        """Ingest Reddit posts using dlt"""
        from ingestion.pipelines.reddit_pipeline import run_reddit_pipeline
        return run_reddit_pipeline()
    
    @task
    def ingest_news_data():
        """Ingest news articles using dlt"""
        from ingestion.pipelines.news_pipeline import run_news_pipeline
        return run_news_pipeline()
    
    @task
    def ingest_finance_data():
        """Ingest stock and finance data using dlt"""
        from ingestion.pipelines.finance_pipeline import run_finance_pipeline
        return run_finance_pipeline()
    
    @task
    def transform_data(reddit_info, news_info, finance_info):
        """Transform data using dbt"""
        import subprocess
        result = subprocess.run(
            ["dbt", "run", "--project-dir", str(project_root / "transformation")],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise Exception(f"dbt run failed: {result.stderr}")
        return result.stdout
    
    @task
    def test_data_quality(transform_result):
        """Run dbt tests for data quality"""
        import subprocess
        result = subprocess.run(
            ["dbt", "test", "--project-dir", str(project_root / "transformation")],
            capture_output=True,
            text=True
        )
        return result.stdout
    
    # Define task dependencies
    reddit = ingest_reddit_data()
    news = ingest_news_data()
    finance = ingest_finance_data()
    
    transform = transform_data(reddit, news, finance)
    test_data_quality(transform)

# Instantiate the DAG
dag_instance = market_intelligence_pipeline()

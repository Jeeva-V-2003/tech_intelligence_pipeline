import dlt
from ingestion.sources.finance_source import stock_quotes, company_news
from config import config

def run_finance_pipeline():
    """Run the finance ingestion pipeline"""
    pipeline = dlt.pipeline(
        pipeline_name="finance_ingestion",
        destination="duckdb",
        dataset_name="raw_finance",
        credentials=config.DUCKDB_PATH
    )
    
    load_info = pipeline.run([stock_quotes(), company_news()])
    print(f"Finance pipeline completed: {load_info}")
    return load_info

if __name__ == "__main__":
    run_finance_pipeline()

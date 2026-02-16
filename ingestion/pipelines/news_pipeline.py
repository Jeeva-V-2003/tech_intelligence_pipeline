import dlt
from ingestion.sources.news_source import news_articles
from config import config

def run_news_pipeline():
    """Run the news ingestion pipeline"""
    pipeline = dlt.pipeline(
        pipeline_name="news_ingestion",
        destination="duckdb",
        dataset_name="raw_news",
        credentials=config.DUCKDB_PATH
    )
    
    load_info = pipeline.run(news_articles())
    print(f"News pipeline completed: {load_info}")
    return load_info

if __name__ == "__main__":
    run_news_pipeline()

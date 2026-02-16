import dlt
from ingestion.sources.reddit_source import reddit_posts
from config import config

def run_reddit_pipeline():
    """Run the Reddit ingestion pipeline"""
    pipeline = dlt.pipeline(
        pipeline_name="reddit_ingestion",
        destination="duckdb",
        dataset_name="raw_reddit",
        credentials=config.DUCKDB_PATH
    )
    
    load_info = pipeline.run(reddit_posts())
    print(f"Reddit pipeline completed: {load_info}")
    return load_info

if __name__ == "__main__":
    run_reddit_pipeline()

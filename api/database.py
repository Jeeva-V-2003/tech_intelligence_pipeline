import duckdb
from config import config

def get_db_connection():
    return duckdb.connect(config.DUCKDB_PATH, read_only=True)

def query_to_dict(query: str):
    conn = get_db_connection()
    result = conn.execute(query).df().to_dict(orient="records")
    conn.close()
    return result

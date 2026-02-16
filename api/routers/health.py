from fastapi import APIRouter, HTTPException
from api.database import get_db_connection

router = APIRouter()

@router.get("/health")
def health_check():
    """Check API and database health"""
    try:
        conn = get_db_connection()
        conn.execute("SELECT 1").fetchone()
        conn.close()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database error: {str(e)}")

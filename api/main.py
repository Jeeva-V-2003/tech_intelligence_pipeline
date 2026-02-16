from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import trends, sentiment

app = FastAPI(title="AI Market Intelligence Hub", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(trends.router, prefix="/api", tags=["trends"])
app.include_router(sentiment.router, prefix="/api", tags=["sentiment"])

@app.get("/")
def root():
    return {"message": "AI Market Intelligence Hub API", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "healthy"}

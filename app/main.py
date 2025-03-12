from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from routers import ingest, insights, ai_insights, auth
from config import settings
from logger import logger


# FastAPI app
app = FastAPI(title="Customer Support Insights API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers for data ingestion and insights endpoints
app.include_router(ingest.router, prefix="/ingest", tags=["Ingestion"])
app.include_router(insights.router, prefix="/companies", tags=["Insights"])
app.include_router(ai_insights.router, prefix="/companies", tags=["AI Insights"])
app.include_router(auth.router, prefix="/auth", tags=["Authorization"])

# Every http request forwarded
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
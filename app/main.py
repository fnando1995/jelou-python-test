from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import logging
import uvicorn

from app.routers import ingest, insights, ai_insights
from app.config import settings
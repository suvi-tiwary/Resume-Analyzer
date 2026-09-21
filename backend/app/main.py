import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes.resume import router as resume_router

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("resume_analyzer")

# FastAPI App Instance
app = FastAPI(
    title="Resume Analyzer API",
    description="Backend API for extracting and parsing resume information.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Configuration
# Defaults to Vite development server, expandable via environment variable
cors_env = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
origins = [origin.strip() for origin in cors_env.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(resume_router)


@app.get(
    "/",
    tags=["Root"],
    summary="Root API Status",
    description="Returns the status of the Resume Analyzer API.",
)
async def root():
    return {
        "message": "Resume Analyzer API is running",
        "status": "ok"
    }


@app.get(
    "/health",
    tags=["Health"],
    summary="Health Check",
    description="Health check endpoint for monitoring.",
)
async def health():
    return {
        "status": "healthy"
    }

"""
AURA - AskUrResume-AI Backend
FastAPI application for resume screening and matching
"""
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import resumes, search

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

app = FastAPI(
    title="AURA - AskUrResume-AI",
    description="AI-powered resume screening and matching system",
    version="1.0.0"
)

# Configure CORS to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(resumes.router, prefix="/api/resumes", tags=["Resumes"])
app.include_router(search.router, prefix="/api", tags=["Search"])


@app.get("/")
def root():
    """Root endpoint"""
    return {"message": "Welcome to AURA - AskUrResume-AI API"}


@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

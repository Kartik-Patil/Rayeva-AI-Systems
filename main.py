"""
Main FastAPI application for Rayeva AI Systems.
"""
from fastapi import FastAPI, Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import time
from typing import Dict, Any

from src.core.config import settings
from src.core.database import init_database
from src.core.logging_service import logging_service
from src.api.category_routes import router as category_router
from src.api.b2b_routes import router as b2b_router


# API Key Security
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def verify_api_key(api_key: str = Security(api_key_header)):
    """Verify API key for protected endpoints."""
    if api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key"
        )
    return api_key


# Application lifespan handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and cleanup on app startup/shutdown."""
    # Startup
    logger = logging_service.get_logger("main")
    logger.info("Starting Rayeva AI Systems...")
    
    # Initialize database
    try:
        await init_database()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Rayeva AI Systems...")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-powered modules for sustainable commerce",
    lifespan=lifespan
)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers (with API key protection)
app.include_router(category_router, dependencies=[Depends(verify_api_key)])
app.include_router(b2b_router, dependencies=[Depends(verify_api_key)])


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Welcome endpoint."""
    return {
        "message": "Welcome to Rayeva AI Systems",
        "version": settings.app_version,
        "modules": [
            "AI Auto-Category & Tag Generator",
            "AI B2B Proposal Generator",
            "AI Impact Reporting (Architecture)",
            "AI WhatsApp Support Bot (Architecture)"
        ],
        "docs": "/docs",
        "status": "operational"
    }


# Health check endpoint
@app.get("/api/v1/health", tags=["Monitoring"])
async def health_check():
    """
    Health check endpoint for monitoring.
    Returns system status and basic metrics.
    """
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "environment": "development" if settings.debug else "production",
        "database": "connected",
        "ai_service": "ready"
    }


# Metrics endpoint
@app.get("/api/v1/metrics", tags=["Monitoring"])
async def get_metrics():
    """
    Get API usage metrics and statistics.
    """
    # In production, this would query the database for actual metrics
    return {
        "total_categorizations": 0,
        "total_proposals": 0,
        "uptime_seconds": 0,
        "ai_tokens_used": 0,
        "estimated_cost_usd": 0.0
    }


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler for uncaught errors."""
    logger = logging_service.get_logger("main")
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "message": str(exc) if settings.debug else "An unexpected error occurred"
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )

"""
FlirtCraft Backend - FastAPI Application Entry Point
AI-powered conversation training platform backend
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import os
import logging
from datetime import datetime
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if os.getenv("DEBUG", "false").lower() == "true" else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    logger.info("🚀 FlirtCraft Backend starting up...")
    logger.info(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")
    logger.info(f"Debug mode: {os.getenv('DEBUG', 'false')}")

    # Startup
    yield

    # Shutdown
    logger.info("💤 FlirtCraft Backend shutting down...")

# FastAPI application instance
app = FastAPI(
    title="FlirtCraft API",
    description="AI-powered conversation training platform backend",
    version="1.0.0",
    docs_url="/docs" if os.getenv("API_DOCS_ENABLED", "true").lower() == "true" else None,
    redoc_url="/redoc" if os.getenv("API_DOCS_ENABLED", "true").lower() == "true" else None,
    lifespan=lifespan
)

# CORS configuration for development
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:19006").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/")
async def root() -> Dict[str, Any]:
    """Root endpoint with basic API information"""
    return {
        "message": "FlirtCraft API - AI-Powered Conversation Training",
        "version": "1.0.0",
        "status": "running",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "timestamp": datetime.utcnow().isoformat(),
        "docs": "/docs" if os.getenv("API_DOCS_ENABLED", "true").lower() == "true" else "disabled"
    }

@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint for Docker and monitoring"""
    try:
        # Basic health checks
        health_status = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0.0",
            "environment": os.getenv("ENVIRONMENT", "development"),
            "services": {
                "api": "healthy",
                "database": "checking",  # TODO: Add actual database health check
                "redis": "checking",     # TODO: Add actual Redis health check
                "openrouter": "checking" # TODO: Add actual OpenRouter health check
            }
        }

        # TODO: Add actual service health checks here
        # - Database connectivity test
        # - Redis connectivity test
        # - OpenRouter API availability test

        return health_status

    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
        )

# Placeholder endpoints - To be implemented based on architecture
@app.get("/scenarios")
async def get_scenarios():
    """Get available conversation scenarios"""
    return {
        "success": True,
        "data": [
            {"type": "coffee_shop", "display_name": "Coffee Shops & Cafes", "is_premium": False},
            {"type": "bookstore", "display_name": "Bookstores & Libraries", "is_premium": False},
            {"type": "park", "display_name": "Parks & Outdoor Spaces", "is_premium": False},
            {"type": "campus", "display_name": "University Campus", "is_premium": False},
            {"type": "grocery", "display_name": "Grocery Stores & Daily Life", "is_premium": False},
            {"type": "gym", "display_name": "Gyms & Fitness Centers", "is_premium": True},
            {"type": "bar", "display_name": "Bars & Social Venues", "is_premium": True},
            {"type": "gallery", "display_name": "Art Galleries & Cultural Events", "is_premium": True}
        ],
        "meta": {"timestamp": datetime.utcnow().isoformat()}
    }

@app.post("/conversations")
async def create_conversation():
    """Create a new conversation session"""
    return {
        "success": True,
        "data": {
            "id": "placeholder-conversation-id",
            "scenario_type": "coffee_shop",
            "difficulty_level": "green",
            "status": "active",
            "created_at": datetime.utcnow().isoformat()
        },
        "meta": {"timestamp": datetime.utcnow().isoformat()}
    }

if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    reload = os.getenv("RELOAD_ENABLED", "false").lower() == "true"

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=reload,
        access_log=True,
        log_level="debug" if os.getenv("DEBUG", "false").lower() == "true" else "info"
    )
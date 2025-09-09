"""
FlirtCraft Backend API
======================
FastAPI application entry point for the FlirtCraft conversation practice platform.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import os
import logging

# Import API routers
from app.api.auth_supabase import router as auth_router
from app.api.onboarding import router as onboarding_router  
from app.api.users import router as users_router
from app.database import get_database_health, check_async_database_connection
from app.schemas.base import HealthCheckResponse, ErrorResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI application instance
app = FastAPI(
    title="FlirtCraft API",
    description="Backend API for FlirtCraft - AI-powered conversation practice platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {
            "name": "Authentication",
            "description": "User registration, login, and authentication management"
        },
        {
            "name": "Onboarding", 
            "description": "User onboarding flow and progress tracking"
        },
        {
            "name": "Users",
            "description": "User profile, preferences, and progress management"
        }
    ]
)

# Security middleware
if os.getenv("ENVIRONMENT") == "production":
    app.add_middleware(
        TrustedHostMiddleware, 
        allowed_hosts=os.getenv("ALLOWED_HOSTS", "*").split(",")
    )

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)

# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions with consistent error format."""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse.create(
            message=str(exc.detail),
            code="HTTP_ERROR",
            status_code=exc.status_code
        ).dict()
    )

@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """Handle validation errors."""
    return JSONResponse(
        status_code=422,
        content=ErrorResponse.create(
            message="Validation error",
            code="VALIDATION_ERROR",
            details={"error": str(exc)},
            status_code=422
        ).dict()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle unexpected errors."""
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse.create(
            message="Internal server error",
            code="INTERNAL_ERROR",
            status_code=500
        ).dict()
    )

# Include API routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(onboarding_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")

# Health check endpoint
@app.get("/health", response_model=HealthCheckResponse, tags=["System"])
async def health_check():
    """
    Health check endpoint for monitoring and load balancers.
    
    Returns comprehensive health information including database connectivity.
    """
    try:
        database_health = await get_database_health()
        
        health_response = HealthCheckResponse(
            status="healthy",
            service="flirtcraft-backend",
            version="1.0.0",
            environment=os.getenv("ENVIRONMENT", "development"),
            database=database_health
        )
        
        return health_response
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return HealthCheckResponse(
            status="unhealthy",
            service="flirtcraft-backend", 
            version="1.0.0",
            environment=os.getenv("ENVIRONMENT", "development"),
            database={"status": "unhealthy", "error": str(e)}
        )

# Root endpoint
@app.get("/", tags=["System"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "FlirtCraft Backend API",
        "version": "1.0.0",
        "docs_url": "/docs",
        "health_url": "/health",
        "api_base": "/api/v1",
        "endpoints": {
            "authentication": "/api/v1/auth",
            "onboarding": "/api/v1/onboarding",
            "users": "/api/v1/users"
        }
    }

# Database connectivity test endpoint
@app.get("/api/v1/test/database", tags=["System"])
async def test_database():
    """Test database connectivity."""
    try:
        is_connected = await check_async_database_connection()
        database_health = await get_database_health()
        
        return {
            "message": "Database test completed",
            "connected": is_connected,
            "health": database_health,
            "environment": os.getenv("ENVIRONMENT", "development")
        }
        
    except Exception as e:
        logger.error(f"Database test failed: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail=f"Database connectivity test failed: {str(e)}"
        )

# API status endpoint
@app.get("/api/v1/status", tags=["System"])
async def api_status():
    """Get API status and configuration."""
    return {
        "api_version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "features": {
            "authentication": True,
            "onboarding": True,
            "user_profiles": True,
            "database_migrations": True
        },
        "endpoints": {
            "auth": [
                "POST /api/v1/auth/register",
                "POST /api/v1/auth/login", 
                "POST /api/v1/auth/refresh",
                "POST /api/v1/auth/verify-email",
                "POST /api/v1/auth/reset-password",
                "GET /api/v1/auth/status",
                "POST /api/v1/auth/check-email-availability",
                "POST /api/v1/auth/verify-age"
            ],
            "onboarding": [
                "POST /api/v1/onboarding/sessions",
                "GET /api/v1/onboarding/sessions/{session_id}",
                "POST /api/v1/onboarding/sessions/{session_id}/steps",
                "GET /api/v1/onboarding/sessions/{session_id}/progress",
                "POST /api/v1/onboarding/complete",
                "POST /api/v1/onboarding/sessions/{session_id}/abandon"
            ],
            "users": [
                "GET /api/v1/users/{user_id}/profile",
                "PUT /api/v1/users/{user_id}/profile",
                "PUT /api/v1/users/{user_id}/preferences",
                "PUT /api/v1/users/{user_id}/skill-goals",
                "GET /api/v1/users/{user_id}/progress",
                "GET /api/v1/users/{user_id}/stats",
                "GET /api/v1/users/{user_id}/dashboard",
                "GET /api/v1/users/{user_id}/settings",
                "PUT /api/v1/users/{user_id}/settings"
            ]
        }
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    logger.info("Starting FlirtCraft Backend API...")
    
    # Test database connection
    try:
        is_connected = await check_async_database_connection()
        if is_connected:
            logger.info("Database connection successful")
        else:
            logger.warning("Database connection failed")
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
    
    logger.info("FlirtCraft Backend API started successfully")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown."""
    logger.info("Shutting down FlirtCraft Backend API...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        log_level="info",
        reload=os.getenv("ENVIRONMENT", "development") == "development"
    )
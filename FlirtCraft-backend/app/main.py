"""
FlirtCraft Backend - Main FastAPI Application
Modular application with proper structure and router organization
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
import logging
import traceback
from datetime import datetime
from typing import Dict, Any

# Core imports
from .core.config import settings
from .core.database import create_tables, check_database_health
from .core.supabase_client import supabase_client
from .core.redis_client import redis_client
from .services.openrouter import openrouter_service

# Router imports
from .routers import auth, onboarding, scenarios, conversations, analytics

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    logger.info("🚀 FlirtCraft Backend starting up...")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Debug mode: {settings.debug}")

    try:
        # Try to initialize database tables (non-blocking)
        try:
            create_tables()
            logger.info("✅ Database tables initialized")
        except Exception as db_error:
            logger.warning(f"⚠️ Database initialization failed (will continue): {db_error}")

        # Test Supabase connection (non-blocking)
        try:
            health = supabase_client.health_check()
            if health["connected"]:
                logger.info("✅ Supabase connection established")
            else:
                logger.warning("⚠️ Supabase connection failed")
        except Exception as sb_error:
            logger.warning(f"⚠️ Supabase health check failed (will continue): {sb_error}")

        # Additional startup tasks here
        logger.info("✅ Application startup completed")

    except Exception as e:
        logger.error(f"❌ Critical startup error: {e}")
        # Only raise for truly critical errors
        if "port already in use" in str(e).lower():
            raise
        logger.warning("⚠️ Continuing with degraded functionality")

    yield

    # Shutdown
    logger.info("💤 FlirtCraft Backend shutting down...")


# Create FastAPI application
def create_application() -> FastAPI:
    """Create and configure FastAPI application"""

    app = FastAPI(
        title=settings.app_name,
        description="AI-powered conversation training platform backend",
        version=settings.app_version,
        docs_url="/docs" if settings.api_docs_enabled else None,
        redoc_url="/redoc" if settings.api_docs_enabled else None,
        lifespan=lifespan
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.get_cors_origins(),
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(auth.router, prefix="/api/v1")
    app.include_router(onboarding.router, prefix="/api/v1")
    app.include_router(scenarios.router, prefix="/api/v1")
    app.include_router(conversations.router, prefix="/api/v1")
    app.include_router(analytics.router, prefix="/api/v1")

    # Root endpoint
    @app.get("/")
    async def root() -> Dict[str, Any]:
        """Root endpoint with basic API information"""
        return {
            "message": "FlirtCraft API - AI-Powered Conversation Training",
            "version": settings.app_version,
            "status": "running",
            "environment": settings.environment,
            "timestamp": datetime.utcnow().isoformat(),
            "docs": "/docs" if settings.api_docs_enabled else "disabled",
            "endpoints": {
                "auth": "/api/v1/auth",
                "onboarding": "/api/v1/onboarding",
                "scenarios": "/api/v1/scenarios",
                "conversations": "/api/v1/conversations",
                "analytics": "/api/v1/analytics"
            }
        }

    # Health check endpoint
    @app.get("/health")
    async def health_check() -> Dict[str, Any]:
        """Comprehensive health check endpoint"""
        try:
            # Check database health
            db_health = await check_database_health()

            # Check Supabase health
            supabase_health = supabase_client.health_check()

            # Check OpenRouter health
            openrouter_health = await openrouter_service.health_check()

            # Check Redis health
            redis_health = redis_client.health_check()

            # Core services vs external services
            core_services_healthy = redis_health["connected"]  # Only Redis is truly required
            external_services_healthy = (
                db_health["connected"] and
                supabase_health["connected"] and
                openrouter_health["connected"]
            )

            # Determine overall status
            if core_services_healthy and external_services_healthy:
                status = "healthy"
                status_code = 200
            elif core_services_healthy:
                status = "degraded"  # Core API works but external services may be down
                status_code = 200    # Return 200 for degraded - API is still functional
            else:
                status = "unhealthy"  # Core services are down
                status_code = 503

            health_status = {
                "status": status,
                "timestamp": datetime.utcnow().isoformat(),
                "version": settings.app_version,
                "environment": settings.environment,
                "services": {
                    "api": "healthy",
                    "database": db_health["status"],
                    "supabase": supabase_health["status"],
                    "openrouter": openrouter_health["status"],
                    "redis": redis_health["status"]
                },
                "details": {
                    "database": db_health,
                    "supabase": supabase_health,
                    "openrouter": openrouter_health,
                    "redis": redis_health
                }
            }

            return JSONResponse(content=health_status, status_code=status_code)

        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return JSONResponse(
                content={
                    "status": "unhealthy",
                    "error": str(e),
                    "timestamp": datetime.utcnow().isoformat()
                },
                status_code=503
            )

    # Global exception handlers
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle request validation errors"""
        logger.warning(f"Validation error: {exc}")
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "error": {
                    "type": "validation_error",
                    "message": "Request validation failed",
                    "details": exc.errors()
                },
                "meta": {
                    "timestamp": datetime.utcnow().isoformat(),
                    "path": str(request.url)
                }
            }
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """Handle HTTP exceptions"""
        logger.warning(f"HTTP exception: {exc.status_code} - {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "type": "http_error",
                    "message": exc.detail,
                    "status_code": exc.status_code
                },
                "meta": {
                    "timestamp": datetime.utcnow().isoformat(),
                    "path": str(request.url)
                }
            }
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle general exceptions"""
        logger.error(f"Unhandled exception: {exc}")
        logger.error(traceback.format_exc())

        # Don't expose internal errors in production
        error_detail = str(exc) if settings.debug else "Internal server error"

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": {
                    "type": "internal_error",
                    "message": error_detail
                },
                "meta": {
                    "timestamp": datetime.utcnow().isoformat(),
                    "path": str(request.url)
                }
            }
        )

    # Request logging middleware
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        """Log all requests"""
        start_time = datetime.utcnow()

        # Process request
        response = await call_next(request)

        # Calculate processing time
        process_time = (datetime.utcnow() - start_time).total_seconds()

        # Log request details
        logger.info(
            f"{request.method} {request.url.path} - "
            f"Status: {response.status_code} - "
            f"Time: {process_time:.3f}s"
        )

        return response

    return app


# Create app instance
app = create_application()


# Additional utility endpoints for development
if settings.environment == "development":
    @app.get("/dev/info")
    async def dev_info():
        """Development information endpoint"""
        return {
            "message": "Development environment information",
            "settings": {
                "environment": settings.environment,
                "debug": settings.debug,
                "cors_origins": settings.get_cors_origins(),
                "api_docs_enabled": settings.api_docs_enabled
            },
            "database": {
                "url_configured": bool(settings.database_url),
                "supabase_configured": bool(settings.supabase_url and settings.supabase_key)
            },
            "external_services": {
                "openrouter_configured": bool(settings.openrouter_api_key),
                "redis_configured": bool(settings.redis_url)
            }
        }

    @app.post("/dev/test-error")
    async def test_error():
        """Test error handling"""
        raise Exception("This is a test error for development")


# Export app for uvicorn
__all__ = ["app"]
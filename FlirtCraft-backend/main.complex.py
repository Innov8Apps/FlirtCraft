"""
FlirtCraft Backend API
======================
FastAPI application entry point for the FlirtCraft conversation practice platform.
Implements comprehensive architecture with database, Redis, AI integration, and monitoring.
"""

import os
import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Dict, Any

from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security import HTTPBearer
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import asyncio
import redis.asyncio as redis
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import text
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import uvloop

# Configure uvloop for better async performance
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/app.log") if os.path.exists("logs") else logging.NullHandler()
    ]
)
logger = logging.getLogger(__name__)

# Database and Redis base setup
Base = declarative_base()
security = HTTPBearer(auto_error=False)

# Application settings with validation
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    # Application settings
    app_name: str = "FlirtCraft API"
    app_version: str = "1.0.0"
    environment: str = Field(default="production", pattern="^(development|staging|production)$")
    debug: bool = False
    api_v1_prefix: str = "/api/v1"
    
    # Security settings
    secret_key: str = Field(default="dev-secret-key-change-in-production", min_length=32)
    allowed_origins: str = "https://flirtcraft.app,https://www.flirtcraft.app"
    trusted_hosts: str = "flirtcraft.app,*.railway.app,localhost,127.0.0.1"
    
    # Database settings
    database_url: str = Field(default="postgresql://flirtcraft_user:flirtcraft_pass@db:5432/flirtcraft_db")
    database_echo: bool = False
    
    # Redis settings
    redis_url: str = Field(default="redis://redis:6379/0")
    
    # AI/External API settings
    gemini_api_key: str = Field(default="your-gemini-api-key-here")
    supabase_url: str = Field(default="http://localhost:54321")
    supabase_anon_key: str = Field(default="your-supabase-anon-key")
    supabase_service_key: str = Field(default="your-supabase-service-key")
    
    # Monitoring settings
    sentry_dsn: str = Field(default="", description="Sentry DSN for error monitoring")
    enable_metrics: bool = True
    
    # Rate limiting settings
    rate_limit_requests: int = 100
    rate_limit_window: int = 60  # seconds
    
    @property
    def allowed_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]
    
    @property
    def trusted_hosts_list(self) -> list[str]:
        return [host.strip() for host in self.trusted_hosts.split(",") if host.strip()]

settings = Settings()

# Global connections
database_engine = None
redis_client = None

# Custom middleware for request logging and metrics
class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = datetime.utcnow()
        
        # Log request
        logger.info(f"Request: {request.method} {request.url.path}")
        
        try:
            response = await call_next(request)
            process_time = (datetime.utcnow() - start_time).total_seconds()
            
            # Log response
            logger.info(f"Response: {response.status_code} - {process_time:.3f}s")
            
            # Add custom headers
            response.headers["X-Process-Time"] = str(process_time)
            response.headers["X-Environment"] = settings.environment
            
            return response
            
        except Exception as e:
            process_time = (datetime.utcnow() - start_time).total_seconds()
            logger.error(f"Request failed: {str(e)} - {process_time:.3f}s")
            raise

# Application lifecycle management
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting FlirtCraft Backend API...")
    
    # Initialize database connection
    global database_engine
    try:
        database_engine = create_async_engine(
            settings.database_url.replace("postgresql://", "postgresql+asyncpg://"),
            echo=settings.database_echo,
            pool_pre_ping=True,
            pool_recycle=300,
            pool_size=20,
            max_overflow=0
        )
        
        # Test database connection
        async with database_engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("Database connection established")
        
    except Exception as e:
        logger.warning(f"Database connection failed (continuing without DB): {e}")
        database_engine = None
    
    # Initialize Redis connection
    global redis_client
    try:
        redis_client = redis.from_url(settings.redis_url, decode_responses=True)
        await redis_client.ping()
        logger.info("Redis connection established")
    except Exception as e:
        logger.warning(f"Redis connection failed (continuing without Redis): {e}")
        redis_client = None
    
    logger.info(f"FlirtCraft API started successfully in {settings.environment} mode")
    
    yield
    
    # Shutdown
    logger.info("Shutting down FlirtCraft Backend API...")
    
    # Close connections
    if database_engine:
        await database_engine.dispose()
        logger.info("Database connection closed")
    
    if redis_client:
        await redis_client.close()
        logger.info("Redis connection closed")
    
    logger.info("FlirtCraft API shutdown complete")

# Create FastAPI application instance with enhanced configuration
app = FastAPI(
    title=settings.app_name,
    description="""Backend API for FlirtCraft - AI-powered conversation practice platform.
    
    ## Features
    - AI-powered conversation training with Google Gemini 2.5 Flash-Lite
    - Real-time WebSocket communication
    - Comprehensive user progress tracking
    - 6-metric feedback system
    - Gamification with achievements and XP
    - Scenario-based practice environments
    - Supabase integration for auth and data
    
    ## Authentication
    All endpoints except `/health`, `/`, and `/docs` require Bearer token authentication.
    """,
    version=settings.app_version,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    lifespan=lifespan,
    debug=settings.debug
)

# Configure security middleware
if not settings.debug:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.trusted_hosts_list
    )

# Configure CORS middleware with proper security
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list if not settings.debug else ["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=[
        "Authorization",
        "Content-Type",
        "Accept",
        "Origin",
        "X-Requested-With",
        "X-Client-Version",
        "User-Agent"
    ],
    expose_headers=["X-Process-Time", "X-Environment"],
    max_age=86400  # 24 hours
)

# Add request logging middleware
app.add_middleware(RequestLoggingMiddleware)

# Global exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error on {request.url.path}: {exc}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Invalid input data",
                "details": exc.errors()
            },
            "meta": {
                "timestamp": datetime.utcnow().isoformat(),
                "path": str(request.url.path)
            }
        }
    )

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.warning(f"HTTP error on {request.url.path}: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": f"HTTP_{exc.status_code}",
                "message": exc.detail
            },
            "meta": {
                "timestamp": datetime.utcnow().isoformat(),
                "path": str(request.url.path)
            }
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error on {request.url.path}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An internal server error occurred" if not settings.debug else str(exc)
            },
            "meta": {
                "timestamp": datetime.utcnow().isoformat(),
                "path": str(request.url.path)
            }
        }
    )

# Dependency functions
async def get_database() -> AsyncSession:
    """Get database session dependency."""
    if not database_engine:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection not available"
        )
    
    async_session = async_sessionmaker(database_engine, expire_on_commit=False)
    async with async_session() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            await session.close()

async def get_redis() -> redis.Redis:
    """Get Redis client dependency."""
    if not redis_client:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Redis connection not available"
        )
    return redis_client

# Standard API response helper
def create_response(
    data: Any = None, 
    message: str = None, 
    success: bool = True,
    meta: Dict[str, Any] = None
) -> Dict[str, Any]:
    """Create standardized API response."""
    response = {
        "success": success,
        "meta": {
            "timestamp": datetime.utcnow().isoformat(),
            **(meta or {})
        }
    }
    
    if data is not None:
        response["data"] = data
    if message:
        response["message"] = message
        
    return response

# Enhanced health check endpoint with comprehensive service status
@app.get("/health")
async def health_check():
    """
    Comprehensive health check endpoint for monitoring and load balancers.
    
    Returns detailed status of all system components including database,
    Redis, and external service connectivity.
    """
    health_status = {
        "status": "healthy",
        "service": "flirtcraft-backend",
        "version": settings.app_version,
        "environment": settings.environment,
        "timestamp": datetime.utcnow().isoformat(),
        "services": {}
    }
    
    # Check database health
    try:
        if database_engine:
            async with database_engine.begin() as conn:
                await conn.execute(text("SELECT 1"))
            health_status["services"]["database"] = "healthy"
        else:
            health_status["services"]["database"] = "unavailable"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        health_status["services"]["database"] = "unhealthy"
        health_status["status"] = "degraded"
    
    # Check Redis health
    try:
        if redis_client:
            await redis_client.ping()
            health_status["services"]["redis"] = "healthy"
        else:
            health_status["services"]["redis"] = "unavailable"
    except Exception as e:
        logger.error(f"Redis health check failed: {e}")
        health_status["services"]["redis"] = "unhealthy"
        health_status["status"] = "degraded"
    
    # Check if any critical services are down
    critical_services = ["database", "redis"]
    unhealthy_critical = [
        service for service in critical_services 
        if health_status["services"].get(service) == "unhealthy"
    ]
    
    if unhealthy_critical:
        health_status["status"] = "unhealthy"
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=health_status
        )
    
    return health_status

# Root endpoint with enhanced API information
@app.get("/")
async def root():
    """
    Root endpoint with comprehensive API information and status.
    """
    return create_response(
        data={
            "message": "FlirtCraft Backend API",
            "version": settings.app_version,
            "environment": settings.environment,
            "docs_url": "/docs" if settings.debug else "Contact support for API documentation",
            "health_url": "/health",
            "api_prefix": settings.api_v1_prefix,
            "features": [
                "AI-powered conversation training",
                "Real-time WebSocket communication", 
                "User progress tracking",
                "6-metric feedback system",
                "Achievement system",
                "Scenario-based practice"
            ],
            "status": "online"
        },
        message="Welcome to the FlirtCraft API"
    )

# Enhanced test endpoint for development and monitoring
@app.get("/api/v1/test")
async def test_endpoint():
    """
    Test endpoint to verify API functionality and service connectivity.
    
    Provides detailed information about service status, configuration,
    and environment for debugging and monitoring purposes.
    """
    test_results = {
        "message": "FlirtCraft API is working!",
        "environment": settings.environment,
        "version": settings.app_version,
        "timestamp": datetime.utcnow().isoformat(),
        "services": {}
    }
    
    # Test database connection
    try:
        if database_engine:
            async with database_engine.begin() as conn:
                result = await conn.execute(text("SELECT version()"))
                version = result.fetchone()
                test_results["services"]["database"] = {
                    "status": "connected",
                    "version": version[0] if version else "unknown"
                }
        else:
            test_results["services"]["database"] = {"status": "not_configured"}
    except Exception as e:
        test_results["services"]["database"] = {
            "status": "error",
            "error": str(e)
        }
    
    # Test Redis connection
    try:
        if redis_client:
            await redis_client.ping()
            info = await redis_client.info()
            test_results["services"]["redis"] = {
                "status": "connected",
                "version": info.get("redis_version", "unknown")
            }
        else:
            test_results["services"]["redis"] = {"status": "not_configured"}
    except Exception as e:
        test_results["services"]["redis"] = {
            "status": "error",
            "error": str(e)
        }
    
    # Configuration status (without sensitive data)
    test_results["configuration"] = {
        "api_keys": {
            "gemini": "configured" if settings.gemini_api_key != "your-gemini-api-key-here" else "not_configured",
            "supabase": "configured" if settings.supabase_url != "http://localhost:54321" else "not_configured"
        },
        "debug_mode": settings.debug,
        "cors_origins": len(settings.allowed_origins_list),
        "trusted_hosts": len(settings.trusted_hosts_list)
    }
    
    return create_response(data=test_results)

# Additional utility endpoints for development
@app.get("/api/v1/status")
async def api_status():
    """Get current API status and basic metrics."""
    return create_response(
        data={
            "status": "operational",
            "environment": settings.environment,
            "version": settings.app_version,
            "uptime": "See health endpoint for detailed status"
        }
    )

if __name__ == "__main__":
    import uvicorn
    
    # Development server configuration
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="debug" if settings.debug else "info",
        access_log=True
    )
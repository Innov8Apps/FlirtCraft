# =============================================================================
# FlirtCraft Backend API - Production Dockerfile
# =============================================================================
# Multi-stage build for optimal production deployment on Railway
# Optimized for FastAPI + SQLAlchemy + Redis + Background Tasks
# =============================================================================

# =============================================================================
# Stage 1: Build Dependencies (Builder Stage)
# =============================================================================
FROM python:3.11-slim as builder

# Set build-time metadata
LABEL maintainer="FlirtCraft Team"
LABEL description="FlirtCraft Backend API - FastAPI Application"
LABEL version="1.0.0"

# Set environment variables for build optimization
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies required for building Python packages
# These are only needed during the build stage
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Create and use a virtual environment for better dependency isolation
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies in virtual environment
# Use pip-tools for deterministic builds if available
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# =============================================================================
# Stage 2: Production Runtime (Final Stage)
# =============================================================================
FROM python:3.11-slim as production

# Set production environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    PATH="/opt/venv/bin:$PATH" \
    # FastAPI/Uvicorn production settings
    WEB_CONCURRENCY=4 \
    MAX_WORKERS=4 \
    PORT=8000 \
    HOST=0.0.0.0 \
    # Application environment
    ENVIRONMENT=production \
    # Disable debug mode in production
    DEBUG=false \
    # Redis and database connection settings
    REDIS_URL=${REDIS_URL} \
    DATABASE_URL=${DATABASE_URL} \
    # Security settings
    SECRET_KEY=${SECRET_KEY} \
    # API settings
    API_V1_PREFIX=/api/v1 \
    # Logging configuration
    LOG_LEVEL=info

# Install only runtime system dependencies (minimal attack surface)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create a non-root user for security
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid appuser --shell /bin/bash --create-home appuser

# Copy the virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv

# Create application directory with proper permissions
WORKDIR /app
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Copy application code with proper ownership
COPY --chown=appuser:appuser . .

# Create necessary directories for logs and temp files
RUN mkdir -p /app/logs /app/tmp && \
    chmod 755 /app/logs /app/tmp

# =============================================================================
# Health Check Configuration
# =============================================================================
# Configure health check endpoint for container orchestration
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:${PORT:-8000}/health', timeout=5)" || exit 1

# =============================================================================
# Security and Performance Optimizations
# =============================================================================
# Expose the configurable port (default 8000, Railway uses $PORT)
EXPOSE ${PORT:-8000}

# Set resource limits and optimizations
# These can be overridden by container orchestration
ENV MALLOC_TRIM_THRESHOLD=100000 \
    MALLOC_MMAP_THRESHOLD=131072 \
    # Python memory optimizations
    PYTHONMALLOC=malloc \
    # Uvicorn worker settings for production
    UVICORN_WORKERS=${WEB_CONCURRENCY:-4} \
    UVICORN_HOST=0.0.0.0 \
    UVICORN_PORT=${PORT:-8000} \
    # Enable uvicorn access logs in production
    UVICORN_ACCESS_LOG=true

# =============================================================================
# Application Startup Command
# =============================================================================
# Use uvicorn with optimal production settings
# Supports:
# - Multiple workers for concurrent request handling
# - WebSocket support for real-time features
# - Proper signal handling for graceful shutdowns
# - Access logging for monitoring
# - Automatic worker restarts on failure

CMD ["sh", "-c", "\
    if [ -f main.py ]; then \
        uvicorn main:app \
            --host ${UVICORN_HOST} \
            --port ${UVICORN_PORT} \
            --workers ${UVICORN_WORKERS} \
            --worker-class uvicorn.workers.UvicornWorker \
            --access-log \
            --log-level ${LOG_LEVEL:-info} \
            --no-use-colors \
            --loop uvloop \
            --http httptools; \
    else \
        echo 'Error: main.py not found. Please ensure your FastAPI application is named main.py' && exit 1; \
    fi"]

# =============================================================================
# Production Deployment Notes
# =============================================================================
# This Dockerfile is optimized for:
# 
# 1. Railway Deployment:
#    - Uses $PORT environment variable for dynamic port assignment
#    - Minimal base image for faster cold starts
#    - Health checks for container monitoring
# 
# 2. Security Best Practices:
#    - Non-root user execution
#    - Minimal attack surface with slim base image
#    - No unnecessary system packages in production
# 
# 3. Performance Optimization:
#    - Multi-stage build for smaller final image
#    - Virtual environment for clean dependencies
#    - Uvloop and httptools for enhanced async performance
#    - Configurable worker processes for horizontal scaling
# 
# 4. Monitoring and Observability:
#    - Health check endpoint at /health
#    - Structured logging with configurable levels
#    - Access logs for request monitoring
# 
# 5. Background Task Support:
#    - Redis integration for job queuing (RQ)
#    - Async/await support for concurrent operations
#    - WebSocket support for real-time features
# 
# Environment Variables Required:
# - DATABASE_URL: PostgreSQL connection string (Supabase)
# - REDIS_URL: Redis connection string for caching/queuing
# - SECRET_KEY: Application secret key for JWT/sessions
# - GEMINI_API_KEY: Google Gemini API key for AI features
# - SUPABASE_URL: Supabase project URL
# - SUPABASE_ANON_KEY: Supabase anonymous key
# 
# Optional Environment Variables:
# - PORT: Server port (default: 8000, Railway sets this automatically)
# - WEB_CONCURRENCY: Number of worker processes (default: 4)
# - LOG_LEVEL: Logging level (default: info)
# - ENVIRONMENT: Application environment (default: production)
# 
# Build Command:
# docker build -t flirtcraft-backend .
# 
# Run Command:
# docker run -p 8000:8000 --env-file .env flirtcraft-backend
# =============================================================================
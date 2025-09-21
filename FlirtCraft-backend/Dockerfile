# FlirtCraft Backend - Production Dockerfile
# FastAPI + Python 3.11 with multi-stage build for optimization

#=============================================================================
# Stage 1: Build dependencies and compile wheels
#=============================================================================
FROM python:3.11-slim-bullseye AS builder

# Set build arguments for optimization
ARG PYTHON_VERSION=3.11
ARG PIP_VERSION=23.3.1

# Install system build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Upgrade pip and install wheel for better caching
RUN pip install --no-cache-dir --upgrade pip==$PIP_VERSION wheel setuptools

# Copy requirements first for better Docker layer caching
COPY requirements.txt /tmp/requirements.txt

# Install Python dependencies with optimizations
RUN pip install --no-cache-dir \
    --disable-pip-version-check \
    --prefer-binary \
    -r /tmp/requirements.txt

#=============================================================================
# Stage 2: Production runtime image
#=============================================================================
FROM python:3.11-slim-bullseye AS production

# Set production environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PATH="/opt/venv/bin:$PATH" \
    VIRTUAL_ENV="/opt/venv"

# Install runtime system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    libffi7 \
    libssl1.1 \
    curl \
    ca-certificates \
    tini \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv

# Create non-root user for security
RUN groupadd --gid 1000 appuser && \
    useradd --uid 1000 --gid 1000 --create-home --shell /bin/bash appuser

# Set up application directory
WORKDIR /app

# Copy application source code
COPY --chown=appuser:appuser . .

# Create necessary directories and set permissions
RUN mkdir -p /app/logs /app/tmp && \
    chown -R appuser:appuser /app && \
    chmod -R 755 /app

# Switch to non-root user
USER appuser

# Expose the application port
EXPOSE 8000

# Health check configuration
HEALTHCHECK --interval=30s \
            --timeout=10s \
            --start-period=40s \
            --retries=3 \
            CMD curl -f http://localhost:8000/health || exit 1

# Set up entry point with proper signal handling
ENTRYPOINT ["tini", "--"]

# Production command with optimized uvicorn settings
CMD ["uvicorn", "main:app", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--workers", "1", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--access-log", \
     "--log-level", "info", \
     "--no-use-colors", \
     "--proxy-headers", \
     "--forwarded-allow-ips", "*"]

#=============================================================================
# Metadata and labels for production tracking
#=============================================================================
LABEL maintainer="FlirtCraft Team" \
      version="1.0.0" \
      description="FlirtCraft FastAPI Backend - Production Ready" \
      com.flirtcraft.component="backend-api" \
      com.flirtcraft.environment="production"

# Security: Remove package manager caches and temp files
USER root
RUN apt-get autoremove -y && \
    apt-get autoclean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /root/.cache
USER appuser
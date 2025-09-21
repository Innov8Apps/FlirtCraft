# FlirtCraft Backend - Local Development Setup

AI-powered conversation training platform backend built with FastAPI, designed for local development with hot reloading and quick iteration.

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- `.env` file is already configured with working credentials

### Start Development Environment
```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up -d --build

# Start only backend and Redis (recommended for development)
docker-compose up backend redis

# Start with background worker (optional)
docker-compose --profile with-worker up
```

The API will be available at: http://localhost:8000

### API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- API Status: http://localhost:8000/
- Health Check: http://localhost:8000/health

### Quick Verification
After starting, verify the setup:
```bash
# Check service status
docker-compose ps

# Test API endpoints
curl http://localhost:8000/health
curl http://localhost:8000/

# View logs
docker-compose logs -f backend
```

## 🔧 Configuration

### Environment Variables
The `.env` file is already configured with working development credentials:

```bash
# External APIs (Pre-configured)
OPENROUTER_API_KEY=sk-or-v1-[configured]
SUPABASE_URL=https://uqatccsnlfehzmjujeyo.supabase.co
SUPABASE_ANON_KEY=[configured]
SUPABASE_SERVICE_KEY=[configured]

# Database (Supabase - Pre-configured)
DATABASE_URL=postgresql://[configured]

# Security (Development keys - change in production)
SECRET_KEY=[configured]
JWT_SECRET_KEY=[configured]
```

### ✅ All Issues Fixed
- **Version attribute warning**: Removed obsolete `version: '3.9'` from docker-compose.yml
- **SUPABASE_KEY variable**: Fixed environment variable name mismatch (`SUPABASE_KEY` → `SUPABASE_ANON_KEY`)
- **Service build error**: Resolved build dependencies and Docker configuration
- **Missing files**: Created `main.py`, `worker.py`, and minimal requirements
- **Local development mode**: Optimized for fast iteration with hot reloading

## 🏗️ Architecture

Based on the FlirtCraft technical architecture:

### Core Services
- **FastAPI Backend**: Main API server with hot reloading
- **Redis**: Cache and job queue
- **Background Worker**: Optional for job processing
- **Supabase**: External PostgreSQL database with auth

### Key Features Implemented
- Health check endpoint (`/health`)
- Basic scenario endpoints
- CORS configuration for frontend development
- Environment-based configuration
- Structured logging

## 🐳 Docker Services

### `backend`
- FastAPI application with hot reloading
- Mounts source code for live updates
- Exposed on port 8000

### `redis`
- Redis 7 Alpine for caching and job queue
- Persistent data storage
- Exposed on port 6379

### `worker` (Optional)
- Background job processor
- Same codebase as backend
- Runs with `--profile with-worker`

## 🔍 Development Commands

```bash
# View logs
docker-compose logs -f backend
docker-compose logs -f redis
docker-compose logs -f worker

# Rebuild services
docker-compose build
docker-compose up --build

# Stop services
docker-compose down

# Clean up everything
docker-compose down -v --remove-orphans
```

## 🏥 Health Monitoring

### Health Check
```bash
curl http://localhost:8000/health
```

### Service Status
- Backend: http://localhost:8000/
- API Docs: http://localhost:8000/docs
- Redis: Accessible on localhost:6379

## 📝 Development Notes

### Hot Reloading
The development setup includes:
- Source code mounting for instant updates
- Uvicorn with `--reload` flag
- Debug logging enabled

### CORS Configuration
Pre-configured for common frontend development ports:
- React: http://localhost:3000
- Expo: http://localhost:19006, exp://localhost:19000

### Rate Limiting
Relaxed for development:
- 60 requests per minute
- 10 conversations per hour

## 🚧 Current Implementation Status

### ✅ Completed
- Docker Compose setup for local development
- Basic FastAPI application structure
- Health check endpoints
- Environment configuration
- Hot reloading setup
- Redis integration setup
- Background worker framework

### 🔄 In Progress / TODO
- Database models and migrations
- Authentication integration
- AI service implementation (OpenRouter + Gemini)
- Conversation endpoints
- Real-time WebSocket support
- Complete background job processing

### 📋 Next Steps
1. Implement database models based on architecture
2. Set up Supabase integration
3. Implement OpenRouter AI service
4. Add conversation management endpoints
5. Set up real-time features

## 🆘 Troubleshooting

### Common Issues

**Port 8000 already in use:**
```bash
docker-compose down
# Or change port in docker-compose.yml
```

**Redis connection issues:**
```bash
docker-compose logs redis
# Check Redis is running and accessible
```

**Environment variable warnings:**
```bash
# Ensure all required variables are set in .env
cp .env.example .env
# Edit .env with your actual values
```

**Build failures:**
```bash
# Clean Docker cache
docker system prune -f
docker-compose build --no-cache
```

For additional help, check the logs:
```bash
docker-compose logs -f
```
# FlirtCraft Local Development Setup

## 🚀 Quick Start

Get FlirtCraft running locally in minutes:

```bash
# 1. Clone and enter the project
cd FlirtCraft

# 2. Setup environment
make setup

# 3. Add your API keys to .env file (see API Keys section below)
# Edit .env and add your GEMINI_API_KEY and SUPABASE credentials

# 4. Start all services
make up

# 5. Open your browser
# Backend API: http://localhost:8000
# API Documentation: http://localhost:8000/docs
```

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Docker** (20.10+) - [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose** (1.29+) - Usually included with Docker
- **Make** (optional but recommended) - For convenient development commands
- **Git** - For version control

### Verify Installation
```bash
docker --version          # Should show Docker version 20.10+
docker-compose --version  # Should show version 1.29+
make --version            # Should show GNU Make
```

## 🔧 Detailed Setup Guide

### Step 1: Environment Configuration

1. **Create environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Get required API keys:**

   **Google Gemini AI API:**
   - Visit [Google AI Studio](https://ai.google.dev/)
   - Create/select a project
   - Enable the Gemini API
   - Create an API key
   - Add to `.env`: `GEMINI_API_KEY=your-key-here`

   **Supabase (Database & Auth):**
   - Visit [Supabase](https://supabase.com/)
   - Create a new project
   - Go to Settings > API
   - Copy Project URL and API keys
   - Add to `.env`:
     ```
     SUPABASE_URL=https://your-project.supabase.co
     SUPABASE_ANON_KEY=your-anon-key
     SUPABASE_SERVICE_KEY=your-service-key
     ```

   **Generate Secret Key:**
   ```bash
   # Generate a secure secret key
   openssl rand -base64 32
   # Add to .env: SECRET_KEY=generated-key-here
   ```

3. **Review and customize .env:**
   - Open `.env` in your editor
   - All variables are documented
   - Most have sensible defaults for local development

### Step 2: Build and Start Services

**Using Make (Recommended):**
```bash
make setup    # Initial setup
make up       # Start all services
make logs     # View logs (optional)
```

**Using Docker Compose Directly:**
```bash
docker-compose up --build -d
docker-compose logs -f
```

### Step 3: Verify Setup

1. **Check service status:**
   ```bash
   make status
   # or
   docker-compose ps
   ```

2. **Access services:**
   - **Backend API:** http://localhost:8000
   - **API Documentation:** http://localhost:8000/docs
   - **Database Admin (Adminer):** http://localhost:8080
   - **Redis Admin:** http://localhost:8081

3. **Health check:**
   ```bash
   make health
   # or
   curl http://localhost:8000/health
   ```

## 🏗️ Architecture Overview

Your local environment includes:

```
┌─────────────────────────────────────────────────┐
│                FlirtCraft Local                 │
├─────────────────────────────────────────────────┤
│  Backend API (FastAPI)     │  Port 8000        │
│  - Hot reloading enabled   │  /docs, /redoc    │
│  - Debug mode on           │                   │
├─────────────────────────────────────────────────┤
│  PostgreSQL Database       │  Port 5432        │
│  - Pre-loaded test data    │  User: flirtcraft │
│  - Schema auto-created     │  DB: flirtcraft_db│
├─────────────────────────────────────────────────┤
│  Redis Cache & Queue       │  Port 6379        │
│  - Background jobs         │  Password: none   │
│  - Session storage         │                   │
├─────────────────────────────────────────────────┤
│  RQ Worker                 │  Background       │
│  - Processes AI tasks      │  Auto-restarts    │
│  - Handles notifications   │                   │
├─────────────────────────────────────────────────┤
│  Adminer (DB Admin)        │  Port 8080        │
│  - Database management     │  Login: auto      │
├─────────────────────────────────────────────────┤
│  Redis Commander           │  Port 8081        │
│  - Redis data viewer       │  admin/admin      │
└─────────────────────────────────────────────────┘
```

## 🛠️ Development Workflow

### Daily Development

```bash
# Start working
make up

# View logs from all services
make logs

# View logs from specific service
make logs-backend
make logs-db

# Restart a service after changes
make restart-backend

# Stop working
make down
```

### Code Changes

**Backend Changes:**
- Files in `FlirtCraft-backend/` are automatically mounted
- Code changes trigger automatic server restart
- No need to rebuild containers for Python code changes

**Database Changes:**
- Schema changes need migrations
- Use `make backend-migrations` to generate
- Use `make backend-migrate` to apply

### Working with the Database

```bash
# Connect to database
make db-connect

# Create backup
make db-backup

# Reset database (⚠️ DELETES ALL DATA)
make db-reset
```

### Working with Redis

```bash
# Open Redis CLI
make redis-cli

# View Redis data in browser
# http://localhost:8081 (admin/admin)

# Clear all Redis data
make redis-flush
```

## 🧪 Testing

### Backend Testing

```bash
# Run all tests
make backend-test

# Run specific test file
make backend-shell
pytest tests/test_conversations.py -v

# Test with coverage
pytest --cov=. tests/
```

### API Testing

1. **Interactive API docs:** http://localhost:8000/docs
2. **Using curl:**
   ```bash
   # Health check
   curl http://localhost:8000/health

   # Get scenarios
   curl http://localhost:8000/api/v1/scenarios
   ```

3. **Using Python requests:**
   ```python
   import requests
   response = requests.get('http://localhost:8000/health')
   print(response.json())
   ```

## 🐛 Troubleshooting

### Common Issues

**Port Already in Use:**
```bash
# Check what's using the port
lsof -i :8000  # or :5432, :6379

# Stop conflicting services
sudo service postgresql stop  # if local postgres is running
```

**Permission Denied:**
```bash
# Fix Docker permissions (Linux/Mac)
sudo usermod -aG docker $USER
# Log out and back in

# Windows Docker Desktop: ensure it's running
```

**Environment Variables Not Loading:**
```bash
# Check if .env exists
ls -la .env

# Verify environment
make env-check

# Recreate from template
make setup-env
```

**Database Connection Failed:**
```bash
# Check database status
make logs-db

# Reset database
make db-reset

# Check network
docker network ls
```

**Build Failures:**
```bash
# Clean rebuild
make clean
make build-no-cache

# Complete reset
make clean-all
make setup
```

### Service-Specific Issues

**Backend Issues:**
```bash
# Check backend logs
make logs-backend

# Enter backend container
make backend-shell

# Check Python dependencies
make backend-requirements
```

**Database Issues:**
```bash
# Check database logs
make logs-db

# Connect to database
make db-connect

# View in Adminer: http://localhost:8080
```

**Redis Issues:**
```bash
# Check Redis logs
make logs-redis

# Test Redis connection
make redis-cli
ping  # Should return PONG

# View in Redis Commander: http://localhost:8081
```

### Getting Help

**Debug Information:**
```bash
# Show all service status
make status

# Show service health
make health

# Show URLs
make urls

# Show environment
make env-check
```

## 📱 Frontend Integration

### React Native/Expo Setup

Your FlirtCraft mobile app should connect to:
- **API Base URL:** `http://localhost:8000`
- **WebSocket URL:** `ws://localhost:8000/ws`

For physical device testing:
1. Find your local IP: `ipconfig` (Windows) or `ifconfig` (Mac/Linux)
2. Update `ALLOWED_ORIGINS` in `.env`:
   ```
   ALLOWED_ORIGINS=http://localhost:3000,http://192.168.1.100:8000,exp://192.168.1.100:19000
   ```

### API Endpoints

Key endpoints for frontend development:
```
GET  /health              # Health check
GET  /api/v1/scenarios    # List scenarios
POST /api/v1/conversations # Start conversation
POST /api/v1/conversations/{id}/messages # Send message
GET  /api/v1/users/profile # User profile
```

## 🔄 Advanced Workflows

### Database Migrations

```bash
# Generate migration after model changes
make backend-migrations

# Apply migrations
make backend-migrate

# View migration history
make backend-shell
alembic history
```

### Background Jobs

```bash
# View worker logs
make logs-worker

# Test job processing
make backend-shell
python -c "from rq import Queue; Queue().enqueue(print, 'Hello World')"
```

### Performance Monitoring

```bash
# View Redis stats
make redis-info

# Database performance
make db-connect
SELECT * FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10;
```

## 🚀 Production Notes

This local setup is optimized for development with:
- **Hot reloading enabled**
- **Debug mode on**
- **Detailed logging**
- **CORS enabled for all origins**
- **No authentication on admin tools**

For production deployment:
- Use the production `Dockerfile` (not `Dockerfile.dev`)
- Enable authentication and security measures
- Use proper secrets management
- Configure monitoring and alerting

## 📚 Useful Commands Reference

### Make Commands
```bash
make help           # Show all commands
make setup          # Initial setup
make up            # Start services
make down          # Stop services
make logs          # View logs
make status        # Show status
make clean         # Clean Docker
make reset         # Reset everything
make health        # Check service health
make urls          # Show service URLs
```

### Docker Commands
```bash
docker-compose ps              # Show running containers
docker-compose logs -f backend # Follow backend logs
docker-compose exec backend bash # Enter backend container
docker-compose restart backend  # Restart backend
docker system df               # Show Docker disk usage
```

### Development URLs
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Redoc:** http://localhost:8000/redoc
- **Database Admin:** http://localhost:8080
- **Redis Admin:** http://localhost:8081

---

## 🆘 Need Help?

1. **Check logs first:** `make logs`
2. **Verify environment:** `make env-check`
3. **Reset if needed:** `make reset`
4. **Clean rebuild:** `make clean-all && make setup`

The development environment is designed to be robust and self-healing. Most issues can be resolved by restarting services or doing a clean rebuild.
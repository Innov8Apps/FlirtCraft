# FlirtCraft Backend API

## 🚀 Overview

The FlirtCraft Backend is a comprehensive FastAPI-based application that powers the AI-driven conversation training platform. Built specifically to support the onboarding feature and user management system, it provides secure, scalable APIs for user authentication, multi-step onboarding, AI-powered conversation practice, and real-time analytics.

## ✨ Key Features

### 🔐 Authentication & Security
- **Supabase Auth Integration**: Secure user registration and authentication
- **JWT Token Management**: Access and refresh token handling
- **Email Verification**: Complete email verification flow
- **Row Level Security**: Database-level security with RLS policies
- **Rate Limiting**: Configurable rate limits for API protection

### 🎯 Onboarding System
- **Multi-Step Flow**: Guided onboarding with progress tracking
- **Age Verification**: 18+ compliance with privacy-focused validation
- **User Preferences**: Dating preferences, age ranges, relationship goals
- **Skill Goals**: Personalized conversation skill development tracking
- **Privacy Controls**: Granular privacy and notification settings
- **Completion Analytics**: Detailed onboarding funnel metrics

### 🤖 AI-Powered Conversations
- **OpenRouter Integration**: Advanced AI conversation generation
- **Dynamic Character Creation**: Context-aware AI personalities
- **Scenario-Based Practice**: Coffee shops, bookstores, parks, and more
- **Difficulty Levels**: Green (easy), Yellow (moderate), Red (challenging)
- **Real-Time Feedback**: AI-powered conversation analysis
- **Performance Tracking**: Session scores and improvement suggestions

### 📊 Analytics & Monitoring
- **Real-Time Metrics**: Live dashboard with user activity
- **Onboarding Funnel**: Step-by-step conversion tracking
- **User Engagement**: DAU, WAU, MAU, and retention metrics
- **Conversation Analytics**: Usage patterns and success rates
- **Performance Monitoring**: Service health and response times

### ⚡ Background Processing
- **Redis Job Queue**: Asynchronous task processing
- **Email Notifications**: Welcome emails and verification reminders
- **Analytics Processing**: Event tracking and metric calculation
- **User Progress Updates**: XP, achievements, and level progression

## 🏗️ Architecture

### Technology Stack
- **Framework**: FastAPI 0.104.1 (High-performance async API)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: Supabase Auth with JWT tokens
- **AI Service**: OpenRouter API for conversation generation
- **Caching**: Redis for sessions, caching, and job queues
- **Validation**: Pydantic for request/response validation
- **Containerization**: Docker & Docker Compose

### Service Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI App   │    │   Supabase      │    │   OpenRouter    │
│                 │◄───►│   Auth & DB     │    │   AI Service    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │     Redis       │
                    │  Cache & Jobs   │
                    └─────────────────┘
```

## 🚦 Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- Supabase project
- OpenRouter API key
- Redis instance

### Using Docker Compose (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd FlirtCraft-backend

# Copy and configure environment
cp .env.example .env
# Edit .env with your API keys and configuration

# Start all services
docker-compose up -d

# Verify health
curl http://localhost:8000/health

# View API documentation
open http://localhost:8000/docs
```

### Manual Development Setup

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your configuration

# Run the application
python main.py

# Access the API
open http://localhost:8000/docs
```

## 🔧 Configuration

### Required Environment Variables

```bash
# Application Settings
ENVIRONMENT=development
DEBUG=true
SECRET_KEY=your-256-bit-secret-key

# Database & Auth (Supabase)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key
SUPABASE_SERVICE_KEY=your-supabase-service-key

# AI Integration
OPENROUTER_API_KEY=your-openrouter-api-key

# Redis Configuration
REDIS_URL=redis://localhost:6379

# CORS for Frontend
CORS_ORIGINS=http://localhost:3000,http://localhost:19006
```

### Optional Configuration

```bash
# Email Service
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Monitoring & Analytics
SENTRY_DSN=your-sentry-dsn-for-error-tracking

# Performance Tuning
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
FREE_CONVERSATIONS_PER_DAY=3
PREMIUM_CONVERSATIONS_PER_DAY=50
```

## 📋 API Documentation

Visit http://localhost:8000/docs for interactive API documentation.

### Core Endpoints

#### 🔐 Authentication (`/api/v1/auth`)
```bash
# User Registration
POST /api/v1/auth/register
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "confirm_password": "SecurePass123!",
  "agreed_to_terms": true,
  "agreed_to_privacy": true,
  "marketing_opt_in": false
}

# User Login
POST /api/v1/auth/login
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}

# Email Verification
POST /api/v1/auth/verify-email
{
  "token": "verification-token-from-email"
}

# Get Current User
GET /api/v1/auth/me
Authorization: Bearer <jwt-token>
```

#### 🎯 Onboarding (`/api/v1/onboarding`)
```bash
# Get Onboarding Flow
GET /api/v1/onboarding/flow
Authorization: Bearer <jwt-token>

# Age Verification
POST /api/v1/onboarding/age-verification
{
  "birth_year": 1995
}

# Set Preferences
POST /api/v1/onboarding/preferences
{
  "target_gender": "female",
  "target_age_min": 22,
  "target_age_max": 30,
  "relationship_goal": "dating"
}

# Set Skill Goals
POST /api/v1/onboarding/skill-goals
{
  "primary_skills": ["conversation_starters", "flow_maintenance"],
  "specific_challenges": ["approach_anxiety", "maintaining_interest"],
  "experience_level": "beginner",
  "practice_frequency": "daily"
}

# Complete Onboarding
POST /api/v1/onboarding/complete
```

#### 🎭 Scenarios (`/api/v1/scenarios`)
```bash
# List Available Scenarios
GET /api/v1/scenarios
?include_premium=true

# Get Scenario Details
GET /api/v1/scenarios/coffee_shop

# Generate Scenario Context
POST /api/v1/scenarios/coffee_shop/context
{
  "difficulty_level": "green"
}
```

#### 💬 Conversations (`/api/v1/conversations`)
```bash
# Create New Conversation
POST /api/v1/conversations
{
  "scenario_type": "coffee_shop",
  "difficulty_level": "green"
}

# Send Message
POST /api/v1/conversations/{conversation_id}/messages
{
  "content": "Hi, I love your book choice!"
}

# End Conversation
POST /api/v1/conversations/{conversation_id}/end

# Get Conversation History
GET /api/v1/conversations/{conversation_id}
```

#### 📊 Analytics (`/api/v1/analytics`)
```bash
# Real-Time Dashboard
GET /api/v1/analytics/dashboard

# Onboarding Funnel
GET /api/v1/analytics/onboarding-funnel?date_range=7

# Conversation Metrics
GET /api/v1/analytics/conversations?date_range=30

# User Engagement
GET /api/v1/analytics/engagement?date_range=7
```

## 🏃‍♂️ Development

### Project Structure
```
FlirtCraft-backend/
├── app/
│   ├── core/                    # Core configuration
│   │   ├── config.py           # Application settings
│   │   ├── database.py         # Database configuration
│   │   ├── supabase_client.py  # Supabase integration
│   │   ├── redis_client.py     # Redis client
│   │   └── auth.py             # Authentication logic
│   ├── models/                 # SQLAlchemy models
│   │   └── user.py             # User, Profile, Conversation models
│   ├── schemas/                # Pydantic schemas
│   │   └── user.py             # Request/response validation
│   ├── routers/                # API endpoints
│   │   ├── auth.py             # Authentication endpoints
│   │   ├── onboarding.py       # Onboarding flow
│   │   ├── scenarios.py        # Scenario management
│   │   ├── conversations.py    # Conversation practice
│   │   └── analytics.py        # Analytics & metrics
│   ├── services/               # Business logic
│   │   ├── openrouter.py       # AI integration
│   │   └── analytics.py        # Analytics service
│   └── main.py                 # FastAPI app factory
├── requirements.txt            # Dependencies
├── requirements-dev.txt        # Development dependencies
├── docker-compose.yml          # Development services
├── Dockerfile                  # Production container
├── .env.example               # Environment template
└── README.md                  # This file
```

### Testing

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Type checking
mypy app/

# Code formatting
black app/
isort app/

# Linting
flake8 app/
```

### Development Commands

```bash
# Start development server with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run with debug logging
DEBUG=true python main.py

# Database migrations (if using Alembic)
alembic revision --autogenerate -m "Add user profiles"
alembic upgrade head

# Reset development database
python -c "from app.core.database import create_tables; create_tables()"
```

## 🚀 Deployment

### Docker Production

```bash
# Build production image
docker build -t flirtcraft-backend:latest .

# Run production container
docker run -d \
  --name flirtcraft-backend \
  --env-file .env.production \
  -p 8000:8000 \
  flirtcraft-backend:latest
```

### Docker Compose Production

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      ENVIRONMENT: production
      DEBUG: false
    env_file:
      - .env.production
    depends_on:
      - redis
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  redis_data:
```

## 📊 Monitoring & Observability

### Health Checks

The `/health` endpoint provides comprehensive service status:

```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0",
  "environment": "production",
  "services": {
    "api": "healthy",
    "database": "healthy",
    "supabase": "healthy",
    "openrouter": "healthy",
    "redis": "healthy"
  },
  "details": {
    "database": {
      "status": "healthy",
      "connected": true
    },
    "supabase": {
      "status": "healthy",
      "connected": true
    },
    "openrouter": {
      "status": "healthy",
      "connected": true,
      "models_available": 15
    },
    "redis": {
      "status": "healthy",
      "connected": true,
      "memory_usage": "2.1M",
      "connected_clients": 3
    }
  }
}
```

### Metrics Collection

Automatic tracking of:
- **Request Metrics**: Response times, error rates, throughput
- **User Metrics**: Registration funnel, engagement, retention
- **Business Metrics**: Conversation success rates, premium conversion
- **System Metrics**: Database performance, AI service latency

### Logging

Structured JSON logging with levels:
```python
# Example log entry
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "INFO",
  "service": "flirtcraft-backend",
  "module": "auth",
  "event": "user_registered",
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "metadata": {
    "email": "user@example.com",
    "registration_source": "onboarding"
  }
}
```

## 🔒 Security

### Authentication Flow
1. User registers with email/password
2. Supabase creates auth account
3. Email verification sent
4. User verifies email
5. JWT tokens issued for API access
6. Tokens refresh automatically

### Data Protection
- **Encryption**: All sensitive data encrypted at rest
- **Input Validation**: Comprehensive Pydantic validation
- **SQL Injection Prevention**: SQLAlchemy ORM protection
- **XSS Protection**: Secure headers and content validation
- **Rate Limiting**: Per-user and per-IP rate limits

### Privacy Compliance
- **GDPR Ready**: User data export and deletion
- **Minimal Data Collection**: Only required information stored
- **Consent Management**: Granular privacy controls
- **Data Retention**: Configurable retention policies

## 🆘 Troubleshooting

### Common Issues

#### Database Connection Failed
```bash
# Check Supabase configuration
curl -H "Authorization: Bearer $SUPABASE_KEY" $SUPABASE_URL/rest/v1/users

# Verify environment variables
python -c "from app.core.config import settings; print(settings.supabase_url)"
```

#### OpenRouter API Errors
```bash
# Test API key
curl -H "Authorization: Bearer $OPENROUTER_API_KEY" https://openrouter.ai/api/v1/models

# Check quotas and limits in OpenRouter dashboard
```

#### Redis Connection Issues
```bash
# Test Redis connection
redis-cli -u $REDIS_URL ping

# Check Redis memory usage
redis-cli -u $REDIS_URL info memory
```

## 🤝 Contributing

### Development Workflow
1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Make changes and add tests**
4. **Run test suite**: `pytest`
5. **Check code quality**: `black app/ && flake8 app/`
6. **Commit changes**: `git commit -m 'Add amazing feature'`
7. **Push to branch**: `git push origin feature/amazing-feature`
8. **Open Pull Request**

### Code Standards
- **Python**: Follow PEP 8 with Black formatting
- **Type Hints**: Required for all function signatures
- **Documentation**: Comprehensive docstrings
- **Tests**: Minimum 80% code coverage
- **Security**: No hardcoded secrets or credentials

## 📞 Support

### Getting Help
- **GitHub Issues**: Bug reports and feature requests
- **API Documentation**: `/docs` endpoint for detailed API reference
- **Health Check**: `/health` for service status
- **Development Info**: `/dev/info` for configuration debugging

### Resources
- **Supabase Documentation**: https://supabase.com/docs
- **FastAPI Documentation**: https://fastapi.tiangolo.com
- **OpenRouter API**: https://openrouter.ai/docs
- **Redis Documentation**: https://redis.io/documentation

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built with ❤️ for FlirtCraft - AI-Powered Conversation Training Platform**

*The backend system that powers confident conversations and meaningful connections.*
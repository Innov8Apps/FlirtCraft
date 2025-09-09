# FlirtCraft Backend - Production Deployment Guide

## Overview

This guide covers deploying the FlirtCraft Backend API to production using Railway, with comprehensive DevOps practices including CI/CD, monitoring, and security.

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Mobile App    │────│  Railway CDN    │────│   Backend API   │
│ (React Native)  │    │   (Load Bal.)   │    │   (FastAPI)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                       ┌─────────────────┐    ┌─────────────────┐
                       │     Redis       │    │   PostgreSQL    │
                       │   (Caching)     │    │   (Primary DB)  │
                       └─────────────────┘    └─────────────────┘
                                                        │
                       ┌─────────────────┐    ┌─────────────────┐
                       │    Supabase     │    │     Sentry      │
                       │ (Auth & Data)   │    │  (Monitoring)   │
                       └─────────────────┘    └─────────────────┘
```

## Production Infrastructure

### Core Services

1. **FastAPI Application**
   - Auto-scaling workers (2-4 instances)
   - Health checks and monitoring
   - Request/response logging
   - Rate limiting and security

2. **PostgreSQL Database**
   - Railway-managed with automated backups
   - Connection pooling and optimization
   - Migration management via Alembic

3. **Redis Cache**
   - Session storage and caching
   - Background job queue (RQ)
   - Performance optimization

4. **Monitoring Stack**
   - Sentry for error tracking
   - Railway metrics dashboard
   - Custom health checks

## Deployment Environments

### Environment Strategy

| Environment | Branch    | URL                                    | Purpose                    |
|-------------|-----------|----------------------------------------|----------------------------|
| Development | `develop` | `https://staging-api.flirtcraft.app`  | Feature testing            |
| Staging     | `develop` | `https://staging-api.flirtcraft.app`  | Pre-production testing     |
| Production  | `main`    | `https://api.flirtcraft.app`          | Live production system     |

### Environment Configuration

Each environment has separate:
- Database instances
- Redis instances  
- API keys and secrets
- Monitoring configurations
- Resource allocations

## Railway Deployment

### Prerequisites

1. **Railway Account**
   ```bash
   # Install Railway CLI
   npm install -g @railway/cli
   
   # Login to Railway
   railway login
   ```

2. **GitHub Repository**
   - Connected to Railway project
   - Automatic deployments enabled
   - Environment variables configured

### Initial Deployment Setup

1. **Create Railway Project**
   ```bash
   railway new flirtcraft-backend
   cd flirtcraft-backend
   railway link [project-id]
   ```

2. **Add Database Services**
   ```bash
   # Add PostgreSQL
   railway add postgresql
   
   # Add Redis
   railway add redis
   ```

3. **Configure Environment Variables**
   ```bash
   # Set production environment variables
   railway variables set ENVIRONMENT=production
   railway variables set DEBUG=false
   railway variables set SECRET_KEY=$(openssl rand -base64 32)
   railway variables set GEMINI_API_KEY=your-api-key
   railway variables set SUPABASE_URL=https://your-project.supabase.co
   railway variables set SUPABASE_ANON_KEY=your-anon-key
   railway variables set SUPABASE_SERVICE_KEY=your-service-key
   railway variables set SENTRY_DSN=https://your-sentry-dsn
   ```

4. **Deploy Application**
   ```bash
   railway up
   ```

### Deployment Configuration

The `railway.toml` file contains comprehensive deployment settings:

```toml
[build]
builder = "dockerfile"
dockerfilePath = "Dockerfile"

[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT --workers $RAILWAY_WORKERS"
healthcheckPath = "/health"
restartPolicyType = "ON_FAILURE"

[env]
ENVIRONMENT = "production"
DEBUG = "false"
RAILWAY_WORKERS = "4"
```

## CI/CD Pipeline

### GitHub Actions Workflow

The CI/CD pipeline includes:

1. **Security Scanning**
   - Dependency vulnerability checks
   - Static code analysis (Bandit, Semgrep)
   - License compliance

2. **Code Quality**
   - Formatting (Black, isort)
   - Linting (flake8, mypy, pylint)
   - Type checking

3. **Testing Suite**
   - Unit tests with coverage
   - Integration tests
   - End-to-end API tests
   - Performance testing

4. **Docker Build**
   - Multi-architecture builds
   - Container security scanning
   - Image optimization

5. **Deployment**
   - Staging deployment (develop branch)
   - Production deployment (main branch)
   - Database migrations
   - Health verification

### Pipeline Configuration

```yaml
# .github/workflows/ci-cd-pipeline.yml
name: FlirtCraft Backend CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run security checks
        run: |
          safety check --requirements requirements.txt
          bandit -r . -x tests/
  
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15-alpine
        env:
          POSTGRES_PASSWORD: testpass
          POSTGRES_USER: testuser
          POSTGRES_DB: testdb
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: pytest --cov=app --cov-report=xml
```

## Database Management

### Migration Strategy

1. **Development Migrations**
   ```bash
   # Create new migration
   alembic revision --autogenerate -m "Description"
   
   # Apply migrations locally
   alembic upgrade head
   ```

2. **Production Migrations**
   ```bash
   # Apply migrations via Railway
   railway run alembic upgrade head
   
   # Or via CI/CD pipeline automatically
   ```

### Backup Strategy

1. **Automated Backups**
   - Railway provides automatic daily backups
   - 30-day retention policy
   - Point-in-time recovery

2. **Manual Backups**
   ```bash
   # Create backup
   railway run pg_dump $DATABASE_URL > backup.sql
   
   # Restore backup
   railway run psql $DATABASE_URL < backup.sql
   ```

### Schema Evolution

- **Backward Compatible Changes**: Deploy immediately
- **Breaking Changes**: Blue-green deployment strategy
- **Data Migrations**: Separate migration and deployment phases

## Security Configuration

### Environment Security

1. **Secret Management**
   ```bash
   # Railway environment variables
   railway variables set SECRET_KEY=$(openssl rand -base64 32)
   railway variables set DATABASE_URL=postgresql://...
   railway variables set REDIS_URL=redis://...
   ```

2. **Access Control**
   - Railway team permissions
   - GitHub branch protection rules
   - API rate limiting

### Application Security

1. **HTTPS/TLS**
   - Automatic SSL certificates via Railway
   - HSTS headers enabled
   - Secure cookie settings

2. **Input Validation**
   - Pydantic request validation
   - SQL injection prevention
   - XSS protection

3. **Authentication**
   - JWT token validation
   - Supabase integration
   - Rate limiting per user

## Monitoring & Observability

### Error Tracking

1. **Sentry Configuration**
   ```python
   import sentry_sdk
   from sentry_sdk.integrations.fastapi import FastApiIntegration
   
   sentry_sdk.init(
       dsn=settings.sentry_dsn,
       integrations=[FastApiIntegration()],
       traces_sample_rate=0.1,
       environment=settings.environment
   )
   ```

2. **Error Alerts**
   - Real-time error notifications
   - Performance degradation alerts
   - Custom business logic alerts

### Performance Monitoring

1. **Application Metrics**
   - Request/response times
   - Database query performance
   - AI API latency
   - Cache hit rates

2. **Infrastructure Metrics**
   - CPU and memory usage
   - Database connections
   - Redis operations
   - Network latency

### Health Checks

1. **Endpoint Health Check**
   ```python
   @app.get("/health")
   async def health_check():
       health_status = {
           "status": "healthy",
           "services": {
               "database": await check_database(),
               "redis": await check_redis(),
               "ai_api": await check_gemini_api()
           }
       }
       return health_status
   ```

2. **Railway Health Checks**
   ```toml
   [deploy]
   healthcheckPath = "/health"
   healthcheckTimeout = 30
   healthcheckInterval = 60
   ```

## Performance Optimization

### Application Performance

1. **Database Optimization**
   - Connection pooling (20 connections)
   - Query optimization
   - Index management
   - Connection recycling

2. **Caching Strategy**
   ```python
   # Redis caching
   CACHE_TTL_USER_PROFILE = 3600      # 1 hour
   CACHE_TTL_SCENARIOS = 86400        # 24 hours
   CACHE_TTL_AI_RESPONSES = 7200      # 2 hours
   ```

3. **API Performance**
   - Response compression
   - Pagination for large datasets
   - Async request handling
   - Request/response caching

### Infrastructure Performance

1. **Auto-scaling**
   ```toml
   [scaling]
   enabled = true
   minReplicas = 1
   maxReplicas = 5
   
   [scaling.metrics.cpu]
   targetAverageUtilization = 70
   ```

2. **Resource Allocation**
   ```toml
   [resources]
   memory = "512Mi"
   cpu = "0.5"
   replicas = { min = 1, max = 5 }
   ```

## Disaster Recovery

### Backup Strategy

1. **Database Backups**
   - Automated daily backups
   - Cross-region replication
   - Point-in-time recovery (7 days)

2. **Application State**
   - Redis persistence enabled
   - Session data backup
   - Configuration backup

### Recovery Procedures

1. **Service Outage**
   ```bash
   # Check service status
   railway status
   
   # View logs
   railway logs --follow
   
   # Restart service
   railway redeploy
   ```

2. **Database Recovery**
   ```bash
   # Point-in-time recovery
   railway db:restore --timestamp="2024-01-01T12:00:00Z"
   
   # Backup restoration
   railway run psql $DATABASE_URL < backup.sql
   ```

### Rollback Strategy

1. **Application Rollback**
   ```bash
   # Rollback to previous deployment
   railway rollback
   
   # Rollback to specific deployment
   railway rollback --deployment-id=deployment-123
   ```

2. **Database Rollback**
   ```bash
   # Rollback migrations
   alembic downgrade -1
   
   # Specific revision rollback
   alembic downgrade revision-id
   ```

## Cost Optimization

### Railway Pricing

1. **Resource Planning**
   - Starter Plan: $5/month (512MB RAM, 1 vCPU)
   - Pro Plan: $20/month (8GB RAM, 8 vCPU)
   - Auto-scaling based on usage

2. **Cost Monitoring**
   - Railway usage dashboard
   - Resource utilization alerts
   - Cost optimization recommendations

### Optimization Strategies

1. **Resource Efficiency**
   ```toml
   # Optimize worker count based on traffic
   RAILWAY_WORKERS = { default = "2", production = "4" }
   
   # Database connection pooling
   DATABASE_POOL_SIZE = "20"
   DATABASE_MAX_OVERFLOW = "0"
   ```

2. **Caching Optimization**
   - Reduce database queries
   - Cache expensive computations
   - Optimize AI API usage

## Troubleshooting

### Common Issues

1. **Deployment Failures**
   ```bash
   # Check build logs
   railway logs --deployment
   
   # Check environment variables
   railway variables
   
   # Verify health checks
   curl https://your-app.railway.app/health
   ```

2. **Database Connection Issues**
   ```bash
   # Test database connection
   railway run python -c "
   import asyncio
   from sqlalchemy.ext.asyncio import create_async_engine
   from sqlalchemy import text
   
   async def test_db():
       engine = create_async_engine(os.environ['DATABASE_URL'])
       async with engine.begin() as conn:
           result = await conn.execute(text('SELECT 1'))
           print('Database connection successful')
   
   asyncio.run(test_db())
   "
   ```

3. **Performance Issues**
   ```bash
   # Monitor resource usage
   railway metrics
   
   # Check slow queries
   railway run psql $DATABASE_URL -c "
   SELECT query, mean_exec_time 
   FROM pg_stat_statements 
   ORDER BY mean_exec_time DESC 
   LIMIT 10;
   "
   ```

### Debug Tools

1. **Logging**
   ```bash
   # Application logs
   railway logs --follow
   
   # Filter logs by level
   railway logs --follow | grep ERROR
   ```

2. **Performance Profiling**
   ```bash
   # Memory profiling
   railway run python -m memory_profiler main.py
   
   # CPU profiling
   railway run python -m cProfile main.py
   ```

## Support & Maintenance

### Monitoring Schedule

- **Daily**: Health checks and error rates
- **Weekly**: Performance metrics review  
- **Monthly**: Security updates and dependency audits
- **Quarterly**: Disaster recovery testing

### Update Process

1. **Security Updates**
   - Automated dependency scanning
   - Critical patches within 24 hours
   - Regular security audits

2. **Feature Updates**
   - Staging deployment first
   - Gradual rollout to production
   - Rollback plan ready

### Contact & Support

- **Development Team**: dev@flirtcraft.app
- **Operations Team**: ops@flirtcraft.app  
- **Emergency Hotline**: [Emergency Contact]
- **Documentation**: https://docs.flirtcraft.app

---

## Quick Reference Commands

```bash
# Deployment
railway up                          # Deploy to production
railway up --environment staging    # Deploy to staging

# Monitoring
railway logs --follow              # View application logs
railway metrics                    # View performance metrics
railway status                     # Check deployment status

# Database
railway run alembic upgrade head   # Run migrations
railway db:backup                  # Create database backup
railway db:restore                 # Restore from backup

# Environment
railway variables                  # List environment variables
railway variables set KEY=value    # Set environment variable
railway shell                     # Open remote shell

# Troubleshooting
railway restart                    # Restart application
railway rollback                   # Rollback deployment
railway logs --deployment          # View deployment logs
```

This deployment guide ensures your FlirtCraft backend is production-ready with comprehensive monitoring, security, and scalability features.
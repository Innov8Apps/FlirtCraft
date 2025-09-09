# =============================================================================
# FlirtCraft - Development Makefile
# =============================================================================
# Convenient commands for local development workflow
# Run 'make help' to see all available commands
# =============================================================================

# Default shell
SHELL := /bin/bash

# Colors for output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
PURPLE := \033[0;35m
CYAN := \033[0;36m
WHITE := \033[0;37m
RESET := \033[0m

# Project configuration
PROJECT_NAME := flirtcraft
COMPOSE_FILE := docker-compose.yml
ENV_FILE := .env

# Docker compose command with proper configuration
DOCKER_COMPOSE := docker-compose -f $(COMPOSE_FILE)

# Default target
.DEFAULT_GOAL := help

# =============================================================================
# Help & Information
# =============================================================================

.PHONY: help
help: ## Display this help message
	@echo "$(CYAN)FlirtCraft Development Commands$(RESET)"
	@echo "$(CYAN)================================$(RESET)"
	@echo ""
	@echo "$(GREEN)Quick Start:$(RESET)"
	@echo "  make setup    - Initial project setup"
	@echo "  make up       - Start all services"
	@echo "  make logs     - View all service logs"
	@echo ""
	@echo "$(GREEN)Available Commands:$(RESET)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(YELLOW)%-15s$(RESET) %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "$(GREEN)Service URLs:$(RESET)"
	@echo "  Backend API:    http://localhost:8000"
	@echo "  API Docs:       http://localhost:8000/docs"
	@echo "  Database Admin: http://localhost:8080"
	@echo "  Redis Admin:    http://localhost:8081"

.PHONY: version
version: ## Show project version and info
	@echo "$(CYAN)FlirtCraft Development Environment$(RESET)"
	@echo "$(YELLOW)Project:$(RESET) $(PROJECT_NAME)"
	@echo "$(YELLOW)Compose File:$(RESET) $(COMPOSE_FILE)"
	@echo "$(YELLOW)Environment:$(RESET) $(ENV_FILE)"
	@echo "$(YELLOW)Docker Version:$(RESET) $$(docker --version)"
	@echo "$(YELLOW)Docker Compose Version:$(RESET) $$(docker-compose --version)"

# =============================================================================
# Initial Setup
# =============================================================================

.PHONY: setup
setup: ## Complete initial project setup
	@echo "$(GREEN)Setting up FlirtCraft development environment...$(RESET)"
	@$(MAKE) check-requirements
	@$(MAKE) setup-env
	@$(MAKE) build
	@echo "$(GREEN)✓ Setup complete! Run 'make up' to start services.$(RESET)"

.PHONY: check-requirements
check-requirements: ## Check if required tools are installed
	@echo "$(BLUE)Checking requirements...$(RESET)"
	@command -v docker >/dev/null 2>&1 || { echo "$(RED)✗ Docker is required but not installed$(RESET)"; exit 1; }
	@command -v docker-compose >/dev/null 2>&1 || { echo "$(RED)✗ Docker Compose is required but not installed$(RESET)"; exit 1; }
	@echo "$(GREEN)✓ All requirements satisfied$(RESET)"

.PHONY: setup-env
setup-env: ## Setup environment file from example
	@if [ ! -f $(ENV_FILE) ]; then \
		echo "$(YELLOW)Creating .env file from .env.example...$(RESET)"; \
		cp .env.example $(ENV_FILE); \
		echo "$(GREEN)✓ Created $(ENV_FILE)$(RESET)"; \
		echo "$(YELLOW)⚠ Please edit $(ENV_FILE) and add your API keys$(RESET)"; \
	else \
		echo "$(BLUE)$(ENV_FILE) already exists$(RESET)"; \
	fi

# =============================================================================
# Docker Operations
# =============================================================================

.PHONY: build
build: ## Build all Docker images
	@echo "$(BLUE)Building Docker images...$(RESET)"
	@$(DOCKER_COMPOSE) build
	@echo "$(GREEN)✓ Build complete$(RESET)"

.PHONY: build-no-cache
build-no-cache: ## Build all Docker images without cache
	@echo "$(BLUE)Building Docker images (no cache)...$(RESET)"
	@$(DOCKER_COMPOSE) build --no-cache
	@echo "$(GREEN)✓ Build complete$(RESET)"

.PHONY: up
up: ## Start all services in background
	@echo "$(BLUE)Starting FlirtCraft services...$(RESET)"
	@$(DOCKER_COMPOSE) up -d
	@echo "$(GREEN)✓ Services started$(RESET)"
	@$(MAKE) status

.PHONY: up-build
up-build: ## Start all services and rebuild images
	@echo "$(BLUE)Starting FlirtCraft services with build...$(RESET)"
	@$(DOCKER_COMPOSE) up -d --build
	@echo "$(GREEN)✓ Services started$(RESET)"
	@$(MAKE) status

.PHONY: up-logs
up-logs: ## Start all services and follow logs
	@echo "$(BLUE)Starting FlirtCraft services...$(RESET)"
	@$(DOCKER_COMPOSE) up

.PHONY: down
down: ## Stop and remove all containers
	@echo "$(BLUE)Stopping FlirtCraft services...$(RESET)"
	@$(DOCKER_COMPOSE) down
	@echo "$(GREEN)✓ Services stopped$(RESET)"

.PHONY: down-volumes
down-volumes: ## Stop containers and remove volumes (⚠️ DELETES ALL DATA)
	@echo "$(RED)⚠️  This will DELETE ALL DATA in the database and Redis!$(RESET)"
	@read -p "Are you sure? (y/N): " confirm && [ "$$confirm" = "y" ] || exit 1
	@echo "$(BLUE)Stopping services and removing volumes...$(RESET)"
	@$(DOCKER_COMPOSE) down -v
	@echo "$(GREEN)✓ Services stopped and volumes removed$(RESET)"

.PHONY: restart
restart: ## Restart all services
	@echo "$(BLUE)Restarting FlirtCraft services...$(RESET)"
	@$(DOCKER_COMPOSE) restart
	@echo "$(GREEN)✓ Services restarted$(RESET)"

.PHONY: status
status: ## Show status of all services
	@echo "$(BLUE)Service Status:$(RESET)"
	@$(DOCKER_COMPOSE) ps

# =============================================================================
# Service Management
# =============================================================================

.PHONY: start-backend
start-backend: ## Start only the backend service
	@echo "$(BLUE)Starting backend service...$(RESET)"
	@$(DOCKER_COMPOSE) up -d backend
	@echo "$(GREEN)✓ Backend started$(RESET)"

.PHONY: start-db
start-db: ## Start only the database service
	@echo "$(BLUE)Starting database service...$(RESET)"
	@$(DOCKER_COMPOSE) up -d db
	@echo "$(GREEN)✓ Database started$(RESET)"

.PHONY: start-redis
start-redis: ## Start only the Redis service
	@echo "$(BLUE)Starting Redis service...$(RESET)"
	@$(DOCKER_COMPOSE) up -d redis
	@echo "$(GREEN)✓ Redis started$(RESET)"

.PHONY: restart-backend
restart-backend: ## Restart only the backend service
	@echo "$(BLUE)Restarting backend service...$(RESET)"
	@$(DOCKER_COMPOSE) restart backend
	@echo "$(GREEN)✓ Backend restarted$(RESET)"

.PHONY: restart-db
restart-db: ## Restart only the database service
	@echo "$(BLUE)Restarting database service...$(RESET)"
	@$(DOCKER_COMPOSE) restart db
	@echo "$(GREEN)✓ Database restarted$(RESET)"

# =============================================================================
# Logging & Monitoring
# =============================================================================

.PHONY: logs
logs: ## View logs from all services
	@$(DOCKER_COMPOSE) logs -f

.PHONY: logs-backend
logs-backend: ## View logs from backend service only
	@$(DOCKER_COMPOSE) logs -f backend

.PHONY: logs-db
logs-db: ## View logs from database service only
	@$(DOCKER_COMPOSE) logs -f db

.PHONY: logs-redis
logs-redis: ## View logs from Redis service only
	@$(DOCKER_COMPOSE) logs -f redis

.PHONY: logs-worker
logs-worker: ## View logs from worker service only
	@$(DOCKER_COMPOSE) logs -f worker

.PHONY: logs-tail
logs-tail: ## View last 50 lines of logs from all services
	@$(DOCKER_COMPOSE) logs --tail=50

# =============================================================================
# Database Operations
# =============================================================================

.PHONY: db-connect
db-connect: ## Connect to PostgreSQL database
	@echo "$(BLUE)Connecting to database...$(RESET)"
	@$(DOCKER_COMPOSE) exec db psql -U flirtcraft_user -d flirtcraft_db

.PHONY: db-backup
db-backup: ## Create database backup
	@mkdir -p backups
	@echo "$(BLUE)Creating database backup...$(RESET)"
	@$(DOCKER_COMPOSE) exec db pg_dump -U flirtcraft_user flirtcraft_db > backups/backup_$$(date +%Y%m%d_%H%M%S).sql
	@echo "$(GREEN)✓ Database backup created in backups/$(RESET)"

.PHONY: db-restore
db-restore: ## Restore database from backup (specify BACKUP_FILE=path)
	@if [ -z "$(BACKUP_FILE)" ]; then \
		echo "$(RED)Please specify BACKUP_FILE=path/to/backup.sql$(RESET)"; \
		exit 1; \
	fi
	@echo "$(BLUE)Restoring database from $(BACKUP_FILE)...$(RESET)"
	@$(DOCKER_COMPOSE) exec -T db psql -U flirtcraft_user -d flirtcraft_db < $(BACKUP_FILE)
	@echo "$(GREEN)✓ Database restored$(RESET)"

.PHONY: db-reset
db-reset: ## Reset database (⚠️ DELETES ALL DATA)
	@echo "$(RED)⚠️  This will DELETE ALL DATA in the database!$(RESET)"
	@read -p "Are you sure? (y/N): " confirm && [ "$$confirm" = "y" ] || exit 1
	@echo "$(BLUE)Resetting database...$(RESET)"
	@$(DOCKER_COMPOSE) down db
	@docker volume rm flirtcraft-postgres-data 2>/dev/null || true
	@$(DOCKER_COMPOSE) up -d db
	@echo "$(GREEN)✓ Database reset$(RESET)"

# =============================================================================
# Redis Operations
# =============================================================================

.PHONY: redis-cli
redis-cli: ## Connect to Redis CLI
	@echo "$(BLUE)Connecting to Redis...$(RESET)"
	@$(DOCKER_COMPOSE) exec redis redis-cli

.PHONY: redis-flush
redis-flush: ## Flush all Redis data
	@echo "$(RED)⚠️  This will DELETE ALL DATA in Redis!$(RESET)"
	@read -p "Are you sure? (y/N): " confirm && [ "$$confirm" = "y" ] || exit 1
	@echo "$(BLUE)Flushing Redis data...$(RESET)"
	@$(DOCKER_COMPOSE) exec redis redis-cli FLUSHALL
	@echo "$(GREEN)✓ Redis data flushed$(RESET)"

.PHONY: redis-info
redis-info: ## Show Redis information
	@$(DOCKER_COMPOSE) exec redis redis-cli INFO

# =============================================================================
# Backend Development
# =============================================================================

.PHONY: backend-shell
backend-shell: ## Open shell in backend container
	@$(DOCKER_COMPOSE) exec backend /bin/bash

.PHONY: backend-test
backend-test: ## Run backend tests
	@echo "$(BLUE)Running backend tests...$(RESET)"
	@$(DOCKER_COMPOSE) exec backend pytest -v
	@echo "$(GREEN)✓ Tests completed$(RESET)"

.PHONY: backend-format
backend-format: ## Format backend code with Black
	@echo "$(BLUE)Formatting backend code...$(RESET)"
	@$(DOCKER_COMPOSE) exec backend black .
	@echo "$(GREEN)✓ Code formatted$(RESET)"

.PHONY: backend-lint
backend-lint: ## Lint backend code with flake8
	@echo "$(BLUE)Linting backend code...$(RESET)"
	@$(DOCKER_COMPOSE) exec backend flake8 .
	@echo "$(GREEN)✓ Linting completed$(RESET)"

.PHONY: backend-migrations
backend-migrations: ## Generate database migrations
	@echo "$(BLUE)Generating database migrations...$(RESET)"
	@$(DOCKER_COMPOSE) exec backend alembic revision --autogenerate -m "Auto migration"
	@echo "$(GREEN)✓ Migrations generated$(RESET)"

.PHONY: backend-migrate
backend-migrate: ## Apply database migrations
	@echo "$(BLUE)Applying database migrations...$(RESET)"
	@$(DOCKER_COMPOSE) exec backend alembic upgrade head
	@echo "$(GREEN)✓ Migrations applied$(RESET)"

.PHONY: backend-requirements
backend-requirements: ## Install/update backend Python requirements
	@echo "$(BLUE)Installing backend requirements...$(RESET)"
	@$(DOCKER_COMPOSE) exec backend pip install -r requirements.txt
	@echo "$(GREEN)✓ Requirements installed$(RESET)"

# =============================================================================
# Development Tools
# =============================================================================

.PHONY: clean
clean: ## Clean up Docker resources
	@echo "$(BLUE)Cleaning up Docker resources...$(RESET)"
	@docker system prune -f
	@echo "$(GREEN)✓ Cleanup completed$(RESET)"

.PHONY: clean-all
clean-all: ## Clean up all Docker resources including volumes
	@echo "$(RED)⚠️  This will DELETE ALL Docker resources including volumes!$(RESET)"
	@read -p "Are you sure? (y/N): " confirm && [ "$$confirm" = "y" ] || exit 1
	@echo "$(BLUE)Cleaning up all Docker resources...$(RESET)"
	@$(DOCKER_COMPOSE) down -v
	@docker system prune -a -f --volumes
	@echo "$(GREEN)✓ All resources cleaned$(RESET)"

.PHONY: urls
urls: ## Show all service URLs
	@echo "$(CYAN)FlirtCraft Service URLs:$(RESET)"
	@echo "$(GREEN)Backend API:$(RESET)      http://localhost:8000"
	@echo "$(GREEN)API Documentation:$(RESET) http://localhost:8000/docs"
	@echo "$(GREEN)API Redoc:$(RESET)        http://localhost:8000/redoc"
	@echo "$(GREEN)Database Admin:$(RESET)   http://localhost:8080"
	@echo "$(GREEN)Redis Admin:$(RESET)      http://localhost:8081"
	@echo ""
	@echo "$(CYAN)Database Connection (for external tools):$(RESET)"
	@echo "$(YELLOW)Host:$(RESET)     localhost"
	@echo "$(YELLOW)Port:$(RESET)     5432"
	@echo "$(YELLOW)Database:$(RESET) flirtcraft_db"
	@echo "$(YELLOW)Username:$(RESET) flirtcraft_user"
	@echo "$(YELLOW)Password:$(RESET) flirtcraft_pass"

.PHONY: health
health: ## Check health of all services
	@echo "$(BLUE)Checking service health...$(RESET)"
	@curl -s -o /dev/null -w "Backend API: %{http_code}\n" http://localhost:8000/health || echo "Backend API: DOWN"
	@curl -s -o /dev/null -w "Adminer: %{http_code}\n" http://localhost:8080 || echo "Adminer: DOWN"
	@curl -s -o /dev/null -w "Redis Commander: %{http_code}\n" http://localhost:8081 || echo "Redis Commander: DOWN"

# =============================================================================
# Environment Management
# =============================================================================

.PHONY: env-check
env-check: ## Check environment variables
	@echo "$(BLUE)Checking environment configuration...$(RESET)"
	@if [ -f $(ENV_FILE) ]; then \
		echo "$(GREEN)✓ .env file exists$(RESET)"; \
		echo "$(BLUE)Current configuration:$(RESET)"; \
		grep -v '^#' $(ENV_FILE) | grep -v '^$$' | while read line; do \
			key=$$(echo $$line | cut -d'=' -f1); \
			value=$$(echo $$line | cut -d'=' -f2-); \
			if [[ $$key == *"KEY"* || $$key == *"SECRET"* || $$key == *"PASSWORD"* ]]; then \
				echo "  $(YELLOW)$$key$(RESET)=***hidden***"; \
			else \
				echo "  $(YELLOW)$$key$(RESET)=$$value"; \
			fi; \
		done; \
	else \
		echo "$(RED)✗ .env file not found$(RESET)"; \
		echo "$(YELLOW)Run 'make setup-env' to create it$(RESET)"; \
	fi

.PHONY: env-template
env-template: ## Show environment template with required variables
	@echo "$(CYAN)Required Environment Variables:$(RESET)"
	@echo "$(YELLOW)GEMINI_API_KEY$(RESET)=your-gemini-api-key-here"
	@echo "$(YELLOW)SUPABASE_URL$(RESET)=https://your-project.supabase.co"
	@echo "$(YELLOW)SUPABASE_ANON_KEY$(RESET)=your-supabase-anon-key"
	@echo "$(YELLOW)SECRET_KEY$(RESET)=your-secure-secret-key"
	@echo ""
	@echo "$(GREEN)Get API keys from:$(RESET)"
	@echo "  Gemini API: https://ai.google.dev/"
	@echo "  Supabase: https://supabase.com/dashboard"

# =============================================================================
# Quick Development Workflows
# =============================================================================

.PHONY: dev
dev: up logs ## Start development environment and follow logs

.PHONY: reset
reset: down-volumes up ## Reset entire environment (⚠️ DELETES ALL DATA)

.PHONY: rebuild
rebuild: down build up ## Rebuild and restart all services

.PHONY: fresh-start
fresh-start: clean-all setup up ## Complete fresh start (⚠️ DELETES EVERYTHING)
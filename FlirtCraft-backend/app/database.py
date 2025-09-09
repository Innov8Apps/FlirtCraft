"""
Database configuration and connection management for FlirtCraft.
Supports both PostgreSQL (production) and SQLite (development).
"""

import os
from typing import AsyncGenerator
from contextlib import asynccontextmanager
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base, sessionmaker

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")
ASYNC_DATABASE_URL = os.getenv("ASYNC_DATABASE_URL")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# For development, use SQLite if no PostgreSQL URL provided
if not DATABASE_URL:
    if ENVIRONMENT == "development":
        DATABASE_URL = "sqlite:///./flirtcraft.db"
        ASYNC_DATABASE_URL = "sqlite+aiosqlite:///./flirtcraft.db"
    else:
        raise ValueError("DATABASE_URL must be set in production environment")

# Convert postgres:// to postgresql:// for SQLAlchemy compatibility
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

if ASYNC_DATABASE_URL and ASYNC_DATABASE_URL.startswith("postgres://"):
    ASYNC_DATABASE_URL = ASYNC_DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Create engines
if ENVIRONMENT == "development" and DATABASE_URL.startswith("sqlite"):
    # SQLite configuration for development
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=True  # Enable SQL logging in development
    )
    async_engine = create_async_engine(
        ASYNC_DATABASE_URL or "sqlite+aiosqlite:///./flirtcraft.db",
        echo=True
    )
else:
    # PostgreSQL configuration for production
    engine = create_engine(
        DATABASE_URL,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        echo=False
    )
    async_engine = create_async_engine(
        ASYNC_DATABASE_URL or DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        echo=False
    )

# Session makers
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Import Base from models
from .models.base import Base

# Metadata for migrations
metadata = Base.metadata


def get_db():
    """
    Dependency to get database session.
    Use this for synchronous database operations.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get async database session.
    Use this for asynchronous database operations.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


@asynccontextmanager
async def get_async_db_context():
    """
    Context manager for async database sessions.
    Use this in background tasks or non-FastAPI contexts.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


def create_tables():
    """
    Create all database tables.
    Only used in development with SQLite.
    """
    Base.metadata.create_all(bind=engine)


async def create_tables_async():
    """
    Create all database tables asynchronously.
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def drop_tables():
    """
    Drop all database tables.
    Use with caution - for development only.
    """
    if ENVIRONMENT != "development":
        raise ValueError("drop_tables() can only be used in development environment")
    
    Base.metadata.drop_all(bind=engine)


async def drop_tables_async():
    """
    Drop all database tables asynchronously.
    Use with caution - for development only.
    """
    if ENVIRONMENT != "development":
        raise ValueError("drop_tables_async() can only be used in development environment")
    
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


def check_database_connection():
    """
    Check if database connection is working.
    Returns True if connection is successful, False otherwise.
    """
    try:
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False


async def check_async_database_connection():
    """
    Check if async database connection is working.
    Returns True if connection is successful, False otherwise.
    """
    try:
        from sqlalchemy import text
        async with async_engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"Async database connection failed: {e}")
        return False


# Database health check for monitoring
async def get_database_health():
    """
    Get comprehensive database health information.
    Used by health check endpoints.
    """
    try:
        from sqlalchemy import text
        async with async_engine.begin() as conn:
            result = await conn.execute(text("SELECT 1"))
            
        health = {
            "status": "healthy",
            "database_type": "postgresql" if "postgresql" in DATABASE_URL else "sqlite",
            "environment": ENVIRONMENT,
            "connection": "active"
        }
        
        # Add pool information for PostgreSQL
        if "postgresql" in DATABASE_URL:
            health.update({
                "pool_size": async_engine.pool.size(),
                "checked_in": async_engine.pool.checkedin(),
                "checked_out": async_engine.pool.checkedout(),
            })
            
        return health
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "database_type": "postgresql" if "postgresql" in DATABASE_URL else "sqlite",
            "environment": ENVIRONMENT,
            "connection": "failed"
        }
"""
Database configuration and session management
"""

from sqlalchemy import create_engine, event, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator
import logging
from .config import settings

logger = logging.getLogger(__name__)

# Database URL from Supabase or direct PostgreSQL
DATABASE_URL = settings.database_url or f"postgresql://postgres:[PASSWORD]@{settings.supabase_url.replace('https://', '').replace('.supabase.co', '.supabase.co:5432')}/postgres"

# SQLAlchemy setup with better connection handling
engine = create_engine(
    DATABASE_URL if DATABASE_URL.startswith("postgresql://") else "sqlite:///./flirtcraft_dev.db",
    pool_pre_ping=True,
    pool_recycle=300,
    pool_timeout=30,  # 30 second connection timeout
    connect_args={
        "connect_timeout": 10,  # 10 second connection timeout for PostgreSQL
        "application_name": "flirtcraft-backend"
    } if DATABASE_URL.startswith("postgresql://") else {},
    echo=settings.debug
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base for models
Base = declarative_base()


def get_db() -> Generator:
    """Database dependency for FastAPI"""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


async def check_database_health() -> dict:
    """Check database connection health"""
    try:
        db = SessionLocal()
        # Use text() for SQLAlchemy 2.0+ compatibility
        result = db.execute(text("SELECT 1"))
        result.fetchone()  # Actually fetch the result
        db.close()
        return {
            "status": "healthy",
            "service": "database",
            "connected": True
        }
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return {
            "status": "unhealthy",
            "service": "database",
            "connected": False,
            "error": str(e)
        }


def create_tables():
    """Create all database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables created successfully")
    except Exception as e:
        logger.error(f"❌ Failed to create database tables: {e}")
        raise
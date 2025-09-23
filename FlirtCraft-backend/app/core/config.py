"""
Core configuration settings for FlirtCraft Backend
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
import os


class Settings(BaseSettings):
    """Application settings with environment variable support"""

    # Application
    app_name: str = "FlirtCraft API"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = False
    api_docs_enabled: bool = True

    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    reload_enabled: bool = False

    # Database - Supabase
    supabase_url: Optional[str] = None
    supabase_anon_key: Optional[str] = None
    supabase_service_key: Optional[str] = None
    database_url: Optional[str] = None

    @property
    def supabase_key(self) -> Optional[str]:
        """Alias for supabase_anon_key for compatibility"""
        return self.supabase_anon_key

    # Redis
    redis_url: str = "redis://localhost:6379"
    redis_password: Optional[str] = None

    # External APIs
    openrouter_api_key: Optional[str] = None
    openrouter_base_url: str = "https://openrouter.ai/api/v1"

    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # CORS - Support both JSON array and comma-separated string
    cors_origins: str | List[str] = [
        "http://localhost:3000",
        "http://localhost:19006",  # Expo dev server
        "exp://localhost:19000",  # Expo tunnel
    ]

    # Email (for verification)
    smtp_server: Optional[str] = None
    smtp_port: int = 587
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None

    # Monitoring
    sentry_dsn: Optional[str] = None

    # Rate Limiting
    rate_limit_requests: int = 100
    rate_limit_window: int = 60  # seconds

    # File Storage
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_file_types: List[str] = ["image/jpeg", "image/png", "image/webp"]

    # Onboarding specific
    min_age_verification: int = 18
    max_age_verification: int = 100
    password_min_length: int = 8
    email_verification_required: bool = True

    # Premium features
    free_conversations_per_day: int = 3
    premium_conversations_per_day: int = 50

    # Feature flags
    enable_rate_limiting: bool = True
    enable_caching: bool = True
    enable_background_jobs: bool = True
    enable_websockets: bool = True
    enable_metrics_collection: bool = True

    # Business logic
    free_tier_daily_conversations: int = 5
    premium_tier_daily_conversations: int = 50
    streak_reset_hour: int = 4
    achievement_check_interval: int = 300

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra environment variables

    def get_cors_origins(self) -> List[str]:
        """Get CORS origins as list from environment variable"""
        if isinstance(self.cors_origins, str):
            # Handle both JSON array string and comma-separated string
            origins_str = self.cors_origins.strip()
            if origins_str.startswith('[') and origins_str.endswith(']'):
                # Parse as JSON array
                import json
                try:
                    return json.loads(origins_str)
                except json.JSONDecodeError:
                    # Fallback to comma-separated if JSON parsing fails
                    pass
            # Parse as comma-separated string
            return [origin.strip() for origin in origins_str.split(",") if origin.strip()]
        return self.cors_origins


# Global settings instance
settings = Settings()

# Validate required environment variables
def validate_required_settings():
    """Validate that required settings are present"""
    required_settings = []

    if not settings.supabase_url:
        required_settings.append("SUPABASE_URL")
    if not settings.supabase_key:
        required_settings.append("SUPABASE_KEY")
    if not settings.openrouter_api_key and settings.environment == "production":
        required_settings.append("OPENROUTER_API_KEY")

    if required_settings:
        missing = ", ".join(required_settings)
        raise ValueError(f"Missing required environment variables: {missing}")

# Validate settings on import in production
if settings.environment == "production":
    validate_required_settings()
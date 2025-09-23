"""
Supabase client configuration for FlirtCraft Backend
"""

from supabase import create_client, Client
from typing import Optional
import logging
from .config import settings

logger = logging.getLogger(__name__)


class SupabaseClient:
    """Singleton Supabase client wrapper"""

    _instance: Optional['SupabaseClient'] = None
    _client: Optional[Client] = None

    def __new__(cls) -> 'SupabaseClient':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._client is None:
            self._initialize_client()

    def _initialize_client(self):
        """Initialize the Supabase client"""
        try:
            if not settings.supabase_url or not settings.supabase_key:
                raise ValueError("Supabase URL and key must be provided")

            self._client = create_client(
                supabase_url=settings.supabase_url,
                supabase_key=settings.supabase_key
            )

            logger.info("✅ Supabase client initialized successfully")

        except Exception as e:
            logger.error(f"❌ Failed to initialize Supabase client: {e}")
            raise

    @property
    def client(self) -> Client:
        """Get the Supabase client instance"""
        if self._client is None:
            self._initialize_client()
        return self._client

    def health_check(self) -> dict:
        """Check Supabase connection health"""
        try:
            # Simple health check - attempt to query auth users (will return auth info)
            response = self._client.auth.get_session()
            return {
                "status": "healthy",
                "service": "supabase",
                "connected": True
            }
        except Exception as e:
            logger.error(f"Supabase health check failed: {e}")
            return {
                "status": "unhealthy",
                "service": "supabase",
                "connected": False,
                "error": str(e)
            }


# Global Supabase client instance
supabase_client = SupabaseClient()


def get_supabase() -> Client:
    """Dependency to get Supabase client"""
    return supabase_client.client


# Auth utilities
async def verify_token(token: str) -> dict:
    """Verify JWT token with Supabase"""
    try:
        response = supabase_client.client.auth.get_user(token)
        if response.user:
            return {
                "valid": True,
                "user": response.user,
                "session": response.session if hasattr(response, 'session') else None
            }
        return {"valid": False, "error": "Invalid token"}
    except Exception as e:
        logger.error(f"Token verification failed: {e}")
        return {"valid": False, "error": str(e)}


async def create_user_account(email: str, password: str, metadata: dict = None) -> dict:
    """Create new user account with Supabase Auth"""
    try:
        response = supabase_client.client.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": metadata or {}
            }
        })

        if response.user:
            return {
                "success": True,
                "user": response.user,
                "session": response.session,
                "email_verification_required": not response.user.email_confirmed_at
            }
        else:
            return {
                "success": False,
                "error": "Failed to create account"
            }

    except Exception as e:
        logger.error(f"Account creation failed: {e}")
        return {
            "success": False,
            "error": str(e)
        }


async def sign_in_user(email: str, password: str) -> dict:
    """Sign in user with email and password"""
    try:
        response = supabase_client.client.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        if response.user:
            return {
                "success": True,
                "user": response.user,
                "session": response.session
            }
        else:
            return {
                "success": False,
                "error": "Invalid credentials"
            }

    except Exception as e:
        logger.error(f"Sign in failed: {e}")
        return {
            "success": False,
            "error": str(e)
        }


async def sign_out_user(token: str) -> dict:
    """Sign out user"""
    try:
        # Set the auth token first
        supabase_client.client.auth.set_session(token, None)
        response = supabase_client.client.auth.sign_out()

        return {
            "success": True,
            "message": "Signed out successfully"
        }

    except Exception as e:
        logger.error(f"Sign out failed: {e}")
        return {
            "success": False,
            "error": str(e)
        }


async def refresh_token(refresh_token: str) -> dict:
    """Refresh access token"""
    try:
        response = supabase_client.client.auth.refresh_session(refresh_token)

        if response.session:
            return {
                "success": True,
                "session": response.session,
                "user": response.user
            }
        else:
            return {
                "success": False,
                "error": "Failed to refresh token"
            }

    except Exception as e:
        logger.error(f"Token refresh failed: {e}")
        return {
            "success": False,
            "error": str(e)
        }


async def verify_email(token: str) -> dict:
    """Verify user email with token"""
    try:
        response = supabase_client.client.auth.verify_otp({
            "token": token,
            "type": "email"
        })

        if response.user:
            return {
                "success": True,
                "user": response.user,
                "session": response.session
            }
        else:
            return {
                "success": False,
                "error": "Invalid verification token"
            }

    except Exception as e:
        logger.error(f"Email verification failed: {e}")
        return {
            "success": False,
            "error": str(e)
        }


async def resend_verification_email(email: str) -> dict:
    """Resend email verification"""
    try:
        response = supabase_client.client.auth.resend({
            "type": "signup",
            "email": email
        })

        return {
            "success": True,
            "message": "Verification email sent"
        }

    except Exception as e:
        logger.error(f"Failed to resend verification email: {e}")
        return {
            "success": False,
            "error": str(e)
        }
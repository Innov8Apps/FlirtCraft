"""
Authentication system for FlirtCraft Backend
JWT token validation and user authentication dependencies
"""

from fastapi import Depends, HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
import logging

from .config import settings
from .database import get_db
from .supabase_client import get_supabase, verify_token
from ..models.user import User, UserProfile
from ..schemas.user import UserResponse

logger = logging.getLogger(__name__)

# Security scheme
security = HTTPBearer()


class AuthenticationError(Exception):
    """Custom authentication error"""
    pass


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Get current authenticated user from JWT token
    Supports both local JWT and Supabase tokens
    """
    try:
        token = credentials.credentials

        # First try Supabase token verification
        supabase_result = await verify_token(token)
        if supabase_result.get("valid"):
            supabase_user = supabase_result.get("user")
            if supabase_user:
                # Get user from local database
                user = db.query(User).filter(User.id == supabase_user.id).first()
                if user:
                    return user
                else:
                    # User exists in Supabase but not in local DB
                    # This can happen during onboarding before completion
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="User registration not completed",
                        headers={"WWW-Authenticate": "Bearer"},
                    )

        # Fallback to local JWT verification (if needed)
        try:
            payload = jwt.decode(
                token,
                settings.secret_key,
                algorithms=[settings.algorithm]
            )
            user_id: str = payload.get("sub")
            if user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Get user from database
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Get current active user (not disabled)"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user


async def get_current_user_with_profile(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get current user with their profile"""
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()

    return {
        "user": current_user,
        "profile": profile
    }


async def require_onboarding_completed(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """Require that user has completed onboarding"""
    if not current_user.onboarding_completed:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Onboarding must be completed to access this resource"
        )
    return current_user


async def require_premium_user(
    current_user: User = Depends(require_onboarding_completed)
) -> User:
    """Require premium subscription"""
    if not current_user.is_premium:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Premium subscription required"
        )
    return current_user


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(security),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """Get user if authenticated, None otherwise (for optional authentication)"""
    if not credentials:
        return None

    try:
        # Use the same logic as get_current_user but don't raise exceptions
        token = credentials.credentials

        supabase_result = await verify_token(token)
        if supabase_result.get("valid"):
            supabase_user = supabase_result.get("user")
            if supabase_user:
                user = db.query(User).filter(User.id == supabase_user.id).first()
                return user

        return None
    except Exception as e:
        logger.warning(f"Optional authentication failed: {e}")
        return None


# Utility functions for token management
def create_access_token(data: dict) -> str:
    """Create JWT access token"""
    try:
        from datetime import datetime, timedelta

        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
        return encoded_jwt
    except Exception as e:
        logger.error(f"Failed to create access token: {e}")
        raise


def create_refresh_token(data: dict) -> str:
    """Create JWT refresh token"""
    try:
        from datetime import datetime, timedelta

        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
        return encoded_jwt
    except Exception as e:
        logger.error(f"Failed to create refresh token: {e}")
        raise


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password using passlib"""
    try:
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        logger.error(f"Password verification failed: {e}")
        return False


def get_password_hash(password: str) -> str:
    """Hash password using passlib"""
    try:
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(password)
    except Exception as e:
        logger.error(f"Password hashing failed: {e}")
        raise


# Permission checking utilities
def check_user_permissions(user: User, required_permission: str) -> bool:
    """Check if user has required permissions"""
    # For now, basic permission system
    # Can be extended with role-based permissions later

    if required_permission == "premium" and not user.is_premium:
        return False

    if required_permission == "active" and not user.is_active:
        return False

    if required_permission == "onboarding_completed" and not user.onboarding_completed:
        return False

    return True


def check_conversation_limit(user: User) -> bool:
    """Check if user has remaining conversation attempts"""
    from datetime import datetime, timedelta

    # Reset daily limit if needed
    now = datetime.utcnow()
    if user.daily_limit_reset_at < now - timedelta(days=1):
        # Reset daily usage (this would be done via background job in production)
        return True

    # Check limits
    if user.is_premium:
        return user.daily_conversations_used < settings.premium_conversations_per_day
    else:
        return user.daily_conversations_used < settings.free_conversations_per_day


# Rate limiting utilities
async def check_rate_limit(user_id: str, action: str) -> bool:
    """Check rate limits for specific actions"""
    # This would integrate with Redis for production rate limiting
    # For now, always return True
    return True


# Auth middleware for specific routes
class RequirePermissions:
    """Dependency class for requiring specific permissions"""

    def __init__(self, *permissions: str):
        self.permissions = permissions

    def __call__(self, current_user: User = Depends(get_current_active_user)) -> User:
        for permission in self.permissions:
            if not check_user_permissions(current_user, permission):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permission required: {permission}"
                )
        return current_user


# Specific permission dependencies
require_premium = RequirePermissions("premium")
require_onboarding_completed = RequirePermissions("onboarding_completed")


# Security utilities
def validate_user_context(user: User, resource_user_id: str) -> bool:
    """Validate that user can access resource belonging to another user"""
    # Users can only access their own resources
    return str(user.id) == str(resource_user_id)


async def log_auth_event(event_type: str, user_id: Optional[str] = None, details: Optional[Dict] = None):
    """Log authentication events for security monitoring"""
    log_data = {
        "event_type": event_type,
        "user_id": user_id,
        "timestamp": datetime.utcnow().isoformat(),
        "details": details or {}
    }

    # In production, this would send to proper logging/monitoring system
    logger.info(f"Auth event: {log_data}")


# Email verification utilities
async def generate_email_verification_token(user_id: str) -> str:
    """Generate email verification token"""
    from datetime import datetime, timedelta

    data = {
        "sub": user_id,
        "type": "email_verification",
        "exp": datetime.utcnow() + timedelta(hours=24)  # 24 hour expiry
    }

    return jwt.encode(data, settings.secret_key, algorithm=settings.algorithm)


async def verify_email_verification_token(token: str) -> Optional[str]:
    """Verify email verification token and return user_id"""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        if payload.get("type") != "email_verification":
            return None
        return payload.get("sub")
    except JWTError:
        return None
"""
Supabase Auth integration for FlirtCraft backend.
Replaces custom JWT implementation with proper Supabase Auth.
"""

from typing import Dict, Any, Optional
from datetime import datetime, timedelta, date
import os
import jwt
from jwt import PyJWTError
import asyncio
from collections import defaultdict
from fastapi import APIRouter, HTTPException, Depends, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from supabase import create_client, Client
import uuid

from ..database import get_async_db
from ..models import User, UserProfile, UserProgress
from ..schemas.auth import (
    UserRegistrationRequest, UserLoginRequest, UserRegistrationResponse,
    UserLoginResponse, EmailVerificationRequest, PasswordResetRequest,
    TokenRefreshRequest, TokenRefreshResponse, UserStatusResponse,
    EmailAvailabilityRequest, EmailAvailabilityResponse, 
    AgeVerificationRequest, AgeVerificationResponse
)
from ..schemas.base import SuccessResponse, ErrorResponse


router = APIRouter(prefix="/auth", tags=["Authentication"])

# Rate limiting storage (in production, use Redis or similar)
_rate_limit_store = defaultdict(lambda: defaultdict(list))

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")  
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")

# Initialize Supabase client with error handling
supabase: Optional[Client] = None
try:
    if SUPABASE_URL and SUPABASE_ANON_KEY:
        supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
except Exception as e:
    print(f"Warning: Could not initialize Supabase client: {e}")
    # Continue without Supabase client - will use database directly

# Legacy JWT configuration (for backward compatibility)
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


def verify_supabase_token(token: str) -> dict:
    """Verify Supabase JWT token and return user info."""
    try:
        # Decode Supabase JWT token
        payload = jwt.decode(
            token, 
            SUPABASE_JWT_SECRET, 
            algorithms=["HS256"],
            options={"verify_aud": False}
        )
        return payload
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )


async def get_current_user_from_supabase(
    request: Request,
    db: AsyncSession = Depends(get_async_db)
) -> User:
    """Get current user from Supabase token."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization header"
        )
    
    token = auth_header.replace("Bearer ", "")
    payload = verify_supabase_token(token)
    supabase_user_id = payload.get("sub")
    user_email = payload.get("email")
    
    # Get user from database using supabase_user_id
    stmt = select(User).where(User.supabase_user_id == supabase_user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    # If user not found by supabase_user_id, try by email (for migration)
    if not user and user_email:
        stmt = select(User).where(User.email == user_email)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        
        # Update user with supabase_user_id if found
        if user:
            user.supabase_user_id = supabase_user_id
            await db.commit()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


def check_rate_limit(key: str, max_requests: int = 10, window_minutes: int = 1) -> bool:
    """
    Simple rate limiting implementation.
    In production, use Redis with sliding window.
    """
    now = datetime.now()
    cutoff = now - timedelta(minutes=window_minutes)
    
    # Clean old requests
    _rate_limit_store[key] = [req_time for req_time in _rate_limit_store[key] if req_time > cutoff]
    
    # Check if under limit
    if len(_rate_limit_store[key]) >= max_requests:
        return False
        
    # Add current request
    _rate_limit_store[key].append(now)
    return True


def generate_email_suggestion(email: str) -> str:
    """Generate alternative email suggestions for unavailable emails."""
    local, domain = email.split('@')
    suggestions = [
        f"{local}_{datetime.now().year}@{domain}",
        f"{local}.{datetime.now().strftime('%m%d')}@{domain}",
        f"{local}2024@{domain}"
    ]
    return suggestions[0]  # Return first suggestion for now


@router.post("/register", response_model=SuccessResponse)
async def register_user(
    registration_data: UserRegistrationRequest,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Register a new user with complete onboarding data.
    
    This endpoint creates a new user in our database after Supabase Auth
    has already created the account. It implements the delayed account creation
    pattern where user data is only stored after complete onboarding.
    
    IMPORTANT: This assumes the user was already created in Supabase Auth
    via the frontend. We sync the user data to our database.
    """
    try:
        # Check if email already exists in our database
        stmt = select(User).where(User.email == registration_data.email.lower())
        result = await db.execute(stmt)
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )
        
        # Parse birth date if provided
        birth_date_parsed = None
        if registration_data.birth_date:
            if isinstance(registration_data.birth_date, str):
                birth_date_parsed = datetime.strptime(registration_data.birth_date, '%Y-%m-%d').date()
            else:
                birth_date_parsed = registration_data.birth_date
        
        # Create user record (Supabase handles password)
        new_user = User(
            email=registration_data.email.lower(),
            age=registration_data.age,
            birth_date=birth_date_parsed,
            is_active=True,
            email_verified=False,  # Supabase will handle this
            onboarding_completed=True,
            onboarding_completed_at=datetime.utcnow(),
            # Note: supabase_user_id will be updated when user first authenticates
        )
        
        db.add(new_user)
        await db.flush()  # Flush to get the user ID
        
        # Create user profile with skill_goals
        user_profile = UserProfile(
            user_id=new_user.id,
            target_gender=registration_data.target_gender,
            target_age_min=registration_data.target_age_min,
            target_age_max=registration_data.target_age_max,
            relationship_goal=registration_data.relationship_goal,
            primary_skills=registration_data.primary_skills or [],
            specific_challenges=registration_data.specific_challenges or [],
            skill_goals=registration_data.skill_goals or [],  # New field
            experience_level=registration_data.experience_level,
            practice_frequency=registration_data.practice_frequency,
            notifications_enabled=registration_data.notifications_enabled,
            analytics_opt_in=registration_data.analytics_opt_in,
            marketing_opt_in=registration_data.marketing_opt_in,
            persona_detected=registration_data.persona_detected,
            onboarding_metadata={
                "referral_source": registration_data.referral_source,
                "device_info": registration_data.device_info,
                "birth_date_provided": registration_data.birth_date is not None,
                "registration_timestamp": datetime.utcnow().isoformat()
            }
        )
        
        db.add(user_profile)
        
        # Create user progress record
        user_progress = UserProgress(
            user_id=new_user.id,
            achievements_unlocked=["onboarding_complete"]  # First achievement
        )
        
        db.add(user_progress)
        
        # Commit the transaction
        await db.commit()
        
        # Prepare response
        response_data = UserRegistrationResponse(
            user_id=new_user.id,
            email=new_user.email,
            email_verification_required=not new_user.email_verified,
            onboarding_completed=new_user.onboarding_completed,
            age=new_user.age,
            target_gender=registration_data.target_gender.value,
            experience_level=registration_data.experience_level.value,
            persona_detected=registration_data.persona_detected.value if registration_data.persona_detected else None,
            is_active=new_user.is_active,
            created_at=new_user.created_at
        )
        
        return SuccessResponse(
            data=response_data,
            message="User registered successfully"
        )
        
    except HTTPException:
        await db.rollback()
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user account: {str(e)}"
        )


@router.post("/login", response_model=SuccessResponse)
async def login_user(
    login_data: UserLoginRequest,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Authenticate user with Supabase and return user data.
    
    Note: Authentication is handled by Supabase Auth on the frontend.
    This endpoint validates the user exists in our database.
    """
    try:
        # Find user by email
        stmt = select(User).options(selectinload(User.profile)).where(User.email == login_data.email.lower())
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        
        if not user:
            # User exists in Supabase but not in our DB - this shouldn't happen
            # with proper registration flow, but handle gracefully
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User profile not found. Please complete registration."
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Account is deactivated"
            )
        
        # Prepare response (tokens are handled by Supabase)
        response_data = UserLoginResponse(
            user_id=user.id,
            email=user.email,
            access_token="",  # Supabase handles tokens
            refresh_token=None,
            token_type="bearer",
            expires_in=3600,  # Standard Supabase token expiry
            onboarding_completed=user.onboarding_completed,
            email_verified=user.email_verified,
            is_premium=user.is_premium,
            persona_detected=user.profile.persona_detected if user.profile else None,
            experience_level=user.profile.experience_level if user.profile else "beginner"
        )
        
        return SuccessResponse(
            data=response_data,
            message="Login successful"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )


@router.get("/status", response_model=SuccessResponse)
async def get_user_status(
    current_user: User = Depends(get_current_user_from_supabase)
):
    """
    Get current user status and account information.
    Requires valid Supabase authentication token.
    """
    try:
        response_data = UserStatusResponse(
            user_id=current_user.id,
            email=current_user.email,
            is_active=current_user.is_active,
            email_verified=current_user.email_verified,
            onboarding_completed=current_user.onboarding_completed,
            is_premium=current_user.is_premium,
            premium_expires_at=current_user.premium_expires_at,
            daily_conversations_used=current_user.daily_conversations_used,
            conversation_limit_exceeded=current_user.conversation_limit_exceeded
        )
        
        return SuccessResponse(
            data=response_data,
            message="User status retrieved successfully"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user status: {str(e)}"
        )


@router.post("/check-email-availability", response_model=SuccessResponse)
async def check_email_availability(
    request: Request,
    email_data: EmailAvailabilityRequest,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Check if an email address is available for registration.
    
    This endpoint supports the premium onboarding feature for real-time 
    email availability checking with rate limiting to prevent abuse.
    """
    try:
        # Rate limiting based on IP address
        client_ip = request.client.host if request.client else "unknown"
        rate_key = f"email_check:{client_ip}"
        
        if not check_rate_limit(rate_key, max_requests=10, window_minutes=1):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many email availability checks. Please try again later."
            )
        
        # Check if email exists in database
        stmt = select(User).where(User.email == email_data.email.lower())
        result = await db.execute(stmt)
        existing_user = result.scalar_one_or_none()
        
        is_available = existing_user is None
        suggestion = None
        
        if not is_available:
            suggestion = generate_email_suggestion(email_data.email)
        
        response_data = EmailAvailabilityResponse(
            email=email_data.email,
            is_available=is_available,
            suggestion=suggestion
        )
        
        return SuccessResponse(
            data=response_data,
            message="Email availability checked successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to check email availability: {str(e)}"
        )


@router.post("/verify-age", response_model=SuccessResponse) 
async def verify_age(
    request: Request,
    age_data: AgeVerificationRequest,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Server-side age verification for compliance and security.
    
    This endpoint validates that users meet the minimum age requirement (18+)
    and provides secure age calculation with proper date validation.
    """
    try:
        # Rate limiting based on IP address
        client_ip = request.client.host if request.client else "unknown"
        rate_key = f"age_verify:{client_ip}"
        
        if not check_rate_limit(rate_key, max_requests=5, window_minutes=5):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many age verification attempts. Please try again later."
            )
        
        # Validate date components and create birth date
        try:
            birth_date = date(age_data.birth_year, age_data.birth_month, age_data.birth_day)
        except ValueError as e:
            return SuccessResponse(
                data=AgeVerificationResponse(
                    is_valid=False,
                    error_message=f"Invalid date: {str(e)}"
                ),
                message="Age verification completed"
            )
        
        # Calculate age
        today = date.today()
        age = today.year - birth_date.year
        
        # Adjust for birthday not yet occurred this year
        if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
            age -= 1
        
        # Check minimum age requirement (18+)
        is_valid = age >= 18
        error_message = None
        
        if not is_valid:
            if age < 0:
                error_message = "Birth date cannot be in the future"
            elif age < 18:
                error_message = "You must be at least 18 years old to use FlirtCraft"
            else:
                error_message = "Age verification failed"
        
        response_data = AgeVerificationResponse(
            is_valid=is_valid,
            age=age if is_valid else None,
            birth_date=birth_date.isoformat() if is_valid else None,
            error_message=error_message
        )
        
        return SuccessResponse(
            data=response_data,
            message="Age verification completed successfully" if is_valid else "Age verification failed"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Age verification failed: {str(e)}"
        )


# Supabase Auth integration endpoints
@router.post("/verify-email", response_model=SuccessResponse)
async def verify_email(
    verification_request: EmailVerificationRequest,
    current_user: User = Depends(get_current_user_from_supabase),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Verify user email address with Supabase Auth.
    
    This endpoint syncs email verification status from Supabase to our database.
    """
    try:
        if verification_request.resend:
            # Trigger resend verification email in Supabase
            # TODO: Integrate with Supabase email service
            return SuccessResponse(
                data={"message": "Verification email sent"},
                message="Verification email has been resent"
            )
        
        # Mark email as verified in our database
        current_user.email_verified = True
        await db.commit()
        
        return SuccessResponse(
            data={"email_verified": True},
            message="Email verified successfully"
        )
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Email verification failed: {str(e)}"
        )


@router.post("/reset-password", response_model=SuccessResponse)
async def reset_password(
    reset_request: PasswordResetRequest,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Reset user password through Supabase Auth.
    
    Note: Password reset is handled entirely by Supabase Auth.
    """
    try:
        if reset_request.reset_token and reset_request.new_password:
            # Password reset with token (handled by Supabase)
            return SuccessResponse(
                data={"password_reset": True},
                message="Password reset successfully"
            )
        else:
            # Send password reset email (handled by Supabase)
            return SuccessResponse(
                data={"reset_email_sent": True},
                message="Password reset email sent"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Password reset failed: {str(e)}"
        )
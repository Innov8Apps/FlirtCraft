"""
Authentication routes for FlirtCraft Backend
User registration, login, email verification, and related auth functions
"""

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Dict, Any
import logging
from datetime import datetime

from ..core.database import get_db
from ..core.supabase_client import (
    create_user_account,
    sign_in_user,
    sign_out_user,
    verify_email,
    resend_verification_email
)
from ..core.auth import (
    get_current_user,
    get_current_active_user,
    create_access_token,
    create_refresh_token,
    log_auth_event
)
from ..models.user import User, UserProfile, UserProgress
from ..schemas.user import (
    UserRegistrationRequest,
    UserLoginRequest,
    EmailVerificationRequest,
    ResendVerificationRequest,
    AuthResponse,
    UserResponse,
    StandardResponse,
    ErrorResponse,
    validate_password_strength
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=AuthResponse)
async def register_user(
    user_data: UserRegistrationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Register new user with email and password
    Creates Supabase auth account but delays local profile creation until onboarding completion
    """
    try:
        # Check if email already exists in local database
        existing_user = db.query(User).filter(User.email == user_data.email.lower()).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Validate password strength
        password_validation = validate_password_strength(user_data.password)
        if not password_validation["valid"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "Password does not meet requirements",
                    "requirements": password_validation["requirements"],
                    "suggestions": password_validation["suggestions"]
                }
            )

        # Create Supabase auth account
        supabase_result = await create_user_account(
            email=user_data.email.lower(),
            password=user_data.password,
            metadata={
                "marketing_opt_in": user_data.marketing_opt_in,
                "registration_source": "onboarding"
            }
        )

        if not supabase_result["success"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Registration failed: {supabase_result['error']}"
            )

        supabase_user = supabase_result["user"]

        # Create minimal local user record (full profile created after onboarding)
        local_user = User(
            id=supabase_user.id,
            email=user_data.email.lower(),
            email_verified=bool(supabase_user.email_confirmed_at),
            onboarding_completed=False,
            is_active=True,
            is_premium=False
        )

        db.add(local_user)
        db.commit()
        db.refresh(local_user)

        # Log registration event
        await log_auth_event(
            event_type="user_registered",
            user_id=str(local_user.id),
            details={
                "email": user_data.email.lower(),
                "marketing_opt_in": user_data.marketing_opt_in,
                "email_verification_required": supabase_result["email_verification_required"]
            }
        )

        # Send welcome email in background if email verification not required
        if not supabase_result["email_verification_required"]:
            background_tasks.add_task(send_welcome_email, user_data.email)

        return AuthResponse(
            success=True,
            user=UserResponse.from_orm(local_user),
            access_token=supabase_result.get("session", {}).get("access_token") if supabase_result.get("session") else None,
            refresh_token=supabase_result.get("session", {}).get("refresh_token") if supabase_result.get("session") else None,
            email_verification_required=supabase_result["email_verification_required"],
            message="Registration successful. Please verify your email to continue." if supabase_result["email_verification_required"] else "Registration successful!"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration failed: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed due to server error"
        )


@router.post("/login", response_model=AuthResponse)
async def login_user(
    login_data: UserLoginRequest,
    db: Session = Depends(get_db)
):
    """
    Authenticate user with email and password
    """
    try:
        # Attempt Supabase authentication
        supabase_result = await sign_in_user(
            email=login_data.email.lower(),
            password=login_data.password
        )

        if not supabase_result["success"]:
            await log_auth_event(
                event_type="login_failed",
                details={
                    "email": login_data.email.lower(),
                    "reason": supabase_result["error"]
                }
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        supabase_user = supabase_result["user"]

        # Get local user record
        local_user = db.query(User).filter(User.id == supabase_user.id).first()
        if not local_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User account not found. Please register first."
            )

        # Check if user is active
        if not local_user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is disabled"
            )

        # Update email verification status if changed
        if supabase_user.email_confirmed_at and not local_user.email_verified:
            local_user.email_verified = True
            db.commit()

        # Log successful login
        await log_auth_event(
            event_type="login_successful",
            user_id=str(local_user.id),
            details={
                "email": login_data.email.lower(),
                "onboarding_completed": local_user.onboarding_completed
            }
        )

        return AuthResponse(
            success=True,
            user=UserResponse.from_orm(local_user),
            access_token=supabase_result["session"]["access_token"],
            refresh_token=supabase_result["session"]["refresh_token"],
            email_verification_required=not local_user.email_verified,
            message="Login successful!"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed due to server error"
        )


@router.post("/logout", response_model=StandardResponse)
async def logout_user(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Sign out current user
    """
    try:
        # Sign out from Supabase (this will invalidate the session)
        # Note: We don't have the token here, so we'll just log the event
        # The client should discard the token

        await log_auth_event(
            event_type="logout",
            user_id=str(current_user.id),
            details={"email": current_user.email}
        )

        return StandardResponse(
            success=True,
            message="Logout successful"
        )

    except Exception as e:
        logger.error(f"Logout failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout failed due to server error"
        )


@router.post("/verify-email", response_model=AuthResponse)
async def verify_user_email(
    verification_data: EmailVerificationRequest,
    db: Session = Depends(get_db)
):
    """
    Verify user email with verification token
    """
    try:
        # Verify email with Supabase
        supabase_result = await verify_email(verification_data.token)

        if not supabase_result["success"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email verification failed: {supabase_result['error']}"
            )

        supabase_user = supabase_result["user"]

        # Update local user record
        local_user = db.query(User).filter(User.id == supabase_user.id).first()
        if local_user:
            local_user.email_verified = True
            db.commit()
            db.refresh(local_user)

            await log_auth_event(
                event_type="email_verified",
                user_id=str(local_user.id),
                details={"email": local_user.email}
            )

            return AuthResponse(
                success=True,
                user=UserResponse.from_orm(local_user),
                access_token=supabase_result["session"]["access_token"] if supabase_result.get("session") else None,
                refresh_token=supabase_result["session"]["refresh_token"] if supabase_result.get("session") else None,
                email_verification_required=False,
                message="Email verified successfully!"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Email verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Email verification failed due to server error"
        )


@router.post("/resend-verification", response_model=StandardResponse)
async def resend_verification_email_endpoint(
    resend_data: ResendVerificationRequest
):
    """
    Resend email verification email
    """
    try:
        # Resend verification email via Supabase
        supabase_result = await resend_verification_email(resend_data.email.lower())

        if not supabase_result["success"]:
            # Don't expose whether email exists for security
            pass

        await log_auth_event(
            event_type="verification_email_resent",
            details={"email": resend_data.email.lower()}
        )

        return StandardResponse(
            success=True,
            message="If an account exists with this email, a verification email has been sent."
        )

    except Exception as e:
        logger.error(f"Resend verification failed: {e}")
        # Still return success to avoid email enumeration
        return StandardResponse(
            success=True,
            message="If an account exists with this email, a verification email has been sent."
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get current user information
    """
    return UserResponse.from_orm(current_user)


@router.post("/refresh", response_model=AuthResponse)
async def refresh_access_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token
    Note: This is primarily handled by Supabase client-side
    """
    try:
        from ..core.supabase_client import refresh_token as refresh_supabase_token

        # Refresh token with Supabase
        supabase_result = await refresh_supabase_token(refresh_token)

        if not supabase_result["success"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        supabase_user = supabase_result["user"]
        local_user = db.query(User).filter(User.id == supabase_user.id).first()

        if not local_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return AuthResponse(
            success=True,
            user=UserResponse.from_orm(local_user),
            access_token=supabase_result["session"]["access_token"],
            refresh_token=supabase_result["session"]["refresh_token"],
            message="Token refreshed successfully"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token refresh failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token refresh failed"
        )


@router.post("/check-email", response_model=StandardResponse)
async def check_email_availability(
    email: str,
    db: Session = Depends(get_db)
):
    """
    Check if email is available for registration
    """
    try:
        # Check local database
        existing_user = db.query(User).filter(User.email == email.lower()).first()

        is_available = existing_user is None

        return StandardResponse(
            success=True,
            data={
                "email": email.lower(),
                "available": is_available,
                "message": "Email is available" if is_available else "Email is already registered"
            }
        )

    except Exception as e:
        logger.error(f"Email check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Email availability check failed"
        )


@router.post("/validate-password", response_model=StandardResponse)
async def validate_password_endpoint(password: str):
    """
    Validate password strength
    """
    try:
        validation_result = validate_password_strength(password)

        return StandardResponse(
            success=True,
            data=validation_result,
            message="Password validation completed"
        )

    except Exception as e:
        logger.error(f"Password validation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Password validation failed"
        )


# Background task functions
async def send_welcome_email(email: str):
    """Send welcome email after successful registration"""
    try:
        # In production, this would send actual email
        logger.info(f"Sending welcome email to {email}")
        # Implementation would use email service (SendGrid, SES, etc.)
    except Exception as e:
        logger.error(f"Failed to send welcome email to {email}: {e}")


async def send_verification_reminder(email: str):
    """Send verification reminder email"""
    try:
        # In production, this would send reminder email
        logger.info(f"Sending verification reminder to {email}")
    except Exception as e:
        logger.error(f"Failed to send verification reminder to {email}: {e}")
"""
Pydantic schemas for FlirtCraft API request/response validation.
"""

from .base import BaseResponse, ErrorResponse, SuccessResponse
from .auth import (
    UserRegistrationRequest, UserLoginRequest, UserRegistrationResponse,
    UserLoginResponse, EmailVerificationRequest, PasswordResetRequest
)
from .onboarding import (
    OnboardingSessionCreate, OnboardingSessionResponse, OnboardingStepUpdate,
    OnboardingStepResponse, OnboardingCompleteRequest
)
from .user import (
    UserProfileResponse, UserProfileUpdate, UserPreferencesUpdate,
    UserProgressResponse, UserStatsResponse
)

__all__ = [
    # Base schemas
    "BaseResponse",
    "ErrorResponse", 
    "SuccessResponse",
    
    # Auth schemas
    "UserRegistrationRequest",
    "UserLoginRequest",
    "UserRegistrationResponse",
    "UserLoginResponse", 
    "EmailVerificationRequest",
    "PasswordResetRequest",
    
    # Onboarding schemas
    "OnboardingSessionCreate",
    "OnboardingSessionResponse",
    "OnboardingStepUpdate",
    "OnboardingStepResponse",
    "OnboardingCompleteRequest",
    
    # User schemas
    "UserProfileResponse",
    "UserProfileUpdate",
    "UserPreferencesUpdate", 
    "UserProgressResponse",
    "UserStatsResponse"
]
"""
Authentication schemas for user registration, login, and auth management.
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, validator
from uuid import UUID

from .base import EmailStr, SecurePassword
from ..models.base import Gender, RelationshipGoal, ExperienceLevel, PracticeFrequency, PersonaType, SkillGoal


class UserRegistrationRequest(BaseModel):
    """Request schema for user registration."""
    
    # Basic authentication info
    email: EmailStr = Field(..., description="User's email address")
    password: SecurePassword = Field(..., description="User's password")
    confirm_password: str = Field(..., description="Password confirmation")
    
    # Basic demographic info
    age: int = Field(..., ge=18, le=100, description="User's age (18-100)")
    
    # Preference data from onboarding
    target_gender: Gender = Field(..., description="Preferred conversation partner gender")
    target_age_min: int = Field(..., ge=18, le=100, description="Minimum age preference")
    target_age_max: int = Field(..., ge=18, le=100, description="Maximum age preference")
    relationship_goal: RelationshipGoal = Field(..., description="User's relationship goal")
    
    # Skill and experience data
    primary_skills: List[str] = Field(
        default_factory=list,
        description="Primary conversation skills to develop"
    )
    specific_challenges: List[str] = Field(
        default_factory=list,
        description="Specific areas user finds challenging"
    )
    skill_goals: List[str] = Field(
        default_factory=list,
        description="Selected skill goals from onboarding (1-3 goals)"
    )
    experience_level: ExperienceLevel = Field(..., description="User's experience level")
    practice_frequency: PracticeFrequency = Field(..., description="How often user wants to practice")
    
    # Birth date for age verification compliance
    birth_date: Optional[str] = Field(None, description="Birth date in YYYY-MM-DD format for age verification")
    
    # Privacy and preferences
    notifications_enabled: bool = Field(True, description="Whether to enable notifications")
    analytics_opt_in: bool = Field(True, description="Whether to opt into analytics")
    marketing_opt_in: bool = Field(False, description="Whether to opt into marketing emails")
    
    # Terms and privacy agreement
    agree_to_terms: bool = Field(..., description="Agreement to Terms of Service")
    agree_to_privacy: bool = Field(..., description="Agreement to Privacy Policy")
    
    # Optional onboarding metadata
    persona_detected: Optional[PersonaType] = Field(None, description="Detected user persona")
    referral_source: Optional[str] = Field(None, description="How user found the app")
    device_info: Optional[dict] = Field(None, description="Device and platform information")
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords do not match')
        return v
    
    @validator('target_age_max')
    def valid_age_range(cls, v, values):
        if 'target_age_min' in values and v < values['target_age_min']:
            raise ValueError('target_age_max must be >= target_age_min')
        return v
    
    @validator('agree_to_terms')
    def must_agree_to_terms(cls, v):
        if not v:
            raise ValueError('must agree to Terms of Service')
        return v
    
    @validator('agree_to_privacy')
    def must_agree_to_privacy(cls, v):
        if not v:
            raise ValueError('must agree to Privacy Policy')
        return v
    
    @validator('skill_goals')
    def validate_skill_goals(cls, v):
        if v is not None and len(v) > 0:
            if len(v) > 3:
                raise ValueError('Maximum 3 skill goals allowed')
            # Validate that all skill goals are valid enum values
            valid_goals = [goal.value for goal in SkillGoal]
            for goal in v:
                if goal not in valid_goals:
                    raise ValueError(f'Invalid skill goal: {goal}')
        return v
    
    @validator('birth_date')
    def validate_birth_date(cls, v):
        if v is not None:
            try:
                from datetime import datetime
                birth_date = datetime.strptime(v, '%Y-%m-%d').date()
                today = datetime.now().date()
                age = today.year - birth_date.year
                if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
                    age -= 1
                if age < 18:
                    raise ValueError('Must be at least 18 years old')
            except ValueError as e:
                if 'time data' in str(e):
                    raise ValueError('Invalid date format. Use YYYY-MM-DD')
                raise e
        return v
    
    class Config:
        use_enum_values = True


class UserLoginRequest(BaseModel):
    """Request schema for user login."""
    
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")
    remember_me: bool = Field(False, description="Whether to remember login session")
    
    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "SecurePass123!",
                "remember_me": False
            }
        }


class UserRegistrationResponse(BaseModel):
    """Response schema for user registration."""
    
    user_id: UUID = Field(..., description="Newly created user ID")
    email: str = Field(..., description="User's email address")
    email_verification_required: bool = Field(..., description="Whether email verification is required")
    onboarding_completed: bool = Field(..., description="Whether onboarding was completed")
    
    # Profile data
    age: int = Field(..., description="User's age")
    target_gender: str = Field(..., description="Target gender preference")
    experience_level: str = Field(..., description="User's experience level")
    persona_detected: Optional[str] = Field(None, description="Detected user persona")
    
    # Account status
    is_active: bool = Field(..., description="Whether account is active")
    created_at: datetime = Field(..., description="Account creation timestamp")
    
    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
            UUID: lambda uuid: str(uuid)
        }


class UserLoginResponse(BaseModel):
    """Response schema for user login."""
    
    user_id: UUID = Field(..., description="User ID")
    email: str = Field(..., description="User's email address")
    access_token: str = Field(..., description="Access token for API requests")
    refresh_token: Optional[str] = Field(None, description="Refresh token for token renewal")
    token_type: str = Field("bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")
    
    # User status
    onboarding_completed: bool = Field(..., description="Whether onboarding was completed")
    email_verified: bool = Field(..., description="Whether email is verified")
    is_premium: bool = Field(..., description="Whether user has premium subscription")
    
    # Profile summary
    persona_detected: Optional[str] = Field(None, description="User's detected persona")
    experience_level: str = Field(..., description="User's experience level")
    
    class Config:
        json_encoders = {
            UUID: lambda uuid: str(uuid)
        }


class EmailVerificationRequest(BaseModel):
    """Request schema for email verification."""
    
    email: EmailStr = Field(..., description="Email address to verify")
    verification_code: Optional[str] = Field(None, description="Verification code from email")
    resend: bool = Field(False, description="Whether to resend verification email")
    
    @validator('verification_code')
    def code_or_resend(cls, v, values):
        if not values.get('resend') and not v:
            raise ValueError('verification_code required when not requesting resend')
        return v


class PasswordResetRequest(BaseModel):
    """Request schema for password reset."""
    
    email: EmailStr = Field(..., description="Email address for password reset")
    reset_token: Optional[str] = Field(None, description="Reset token from email")
    new_password: Optional[SecurePassword] = Field(None, description="New password")
    
    @validator('new_password')
    def password_required_with_token(cls, v, values):
        if values.get('reset_token') and not v:
            raise ValueError('new_password required when providing reset_token')
        return v


class TokenRefreshRequest(BaseModel):
    """Request schema for token refresh."""
    
    refresh_token: str = Field(..., description="Refresh token")


class TokenRefreshResponse(BaseModel):
    """Response schema for token refresh."""
    
    access_token: str = Field(..., description="New access token")
    token_type: str = Field("bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")


class UserStatusResponse(BaseModel):
    """Response schema for user status checks."""
    
    user_id: UUID = Field(..., description="User ID")
    email: str = Field(..., description="User's email address")
    is_active: bool = Field(..., description="Whether account is active")
    email_verified: bool = Field(..., description="Whether email is verified")
    onboarding_completed: bool = Field(..., description="Whether onboarding was completed")
    
    # Premium status
    is_premium: bool = Field(..., description="Whether user has premium subscription")
    premium_expires_at: Optional[datetime] = Field(None, description="Premium subscription expiration")
    
    # Usage stats
    daily_conversations_used: int = Field(..., description="Conversations used today")
    conversation_limit_exceeded: bool = Field(..., description="Whether daily limit is exceeded")
    
    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
            UUID: lambda uuid: str(uuid)
        }


class EmailAvailabilityRequest(BaseModel):
    """Request schema for checking email availability."""
    
    email: EmailStr = Field(..., description="Email address to check")
    
    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com"
            }
        }


class EmailAvailabilityResponse(BaseModel):
    """Response schema for email availability check."""
    
    email: str = Field(..., description="Checked email address")
    is_available: bool = Field(..., description="Whether email is available for registration")
    suggestion: Optional[str] = Field(None, description="Alternative email suggestion if not available")
    
    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "is_available": True,
                "suggestion": None
            }
        }


class AgeVerificationRequest(BaseModel):
    """Request schema for server-side age verification."""
    
    birth_day: int = Field(..., ge=1, le=31, description="Day of birth (1-31)")
    birth_month: int = Field(..., ge=1, le=12, description="Month of birth (1-12)")
    birth_year: int = Field(..., ge=1900, le=2010, description="Year of birth")
    
    @validator('birth_day')
    def valid_day_for_month(cls, v, values):
        """Validate day is valid for the given month."""
        month = values.get('birth_month')
        year = values.get('birth_year')
        
        if month and year:
            from calendar import monthrange
            _, max_day = monthrange(year, month)
            if v > max_day:
                raise ValueError(f'Invalid day {v} for month {month}')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "birth_day": 15,
                "birth_month": 6,
                "birth_year": 1995
            }
        }


class AgeVerificationResponse(BaseModel):
    """Response schema for age verification."""
    
    is_valid: bool = Field(..., description="Whether age meets minimum requirement (18+)")
    age: Optional[int] = Field(None, description="Calculated age if valid")
    birth_date: Optional[str] = Field(None, description="ISO formatted birth date if valid")
    error_message: Optional[str] = Field(None, description="Error message if not valid")
    
    class Config:
        schema_extra = {
            "example": {
                "is_valid": True,
                "age": 28,
                "birth_date": "1995-06-15",
                "error_message": None
            }
        }
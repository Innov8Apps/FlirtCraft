"""
Pydantic schemas for user-related API endpoints
Request/response validation for onboarding system
"""

from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


# Enums for validation
class TargetGender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    EVERYONE = "everyone"


class RelationshipGoal(str, Enum):
    DATING = "dating"
    RELATIONSHIPS = "relationships"
    PRACTICE = "practice"
    CONFIDENCE = "confidence"


class ExperienceLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    RETURNING = "returning"


class PracticeFrequency(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    OCCASIONAL = "occasional"


class PrivacyLevel(str, Enum):
    STANDARD = "standard"
    ENHANCED = "enhanced"


class DetectedPersona(str, Enum):
    ANXIOUS_ALEX = "anxiousAlex"
    COMEBACK_CATHERINE = "comebackCatherine"
    CONFIDENT_CARLOS = "confidentCarlos"
    SHY_SARAH = "shySarah"


# Authentication Schemas
class UserRegistrationRequest(BaseModel):
    """User registration request schema"""
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, max_length=128, description="User's password")
    confirm_password: str = Field(..., description="Password confirmation")
    agreed_to_terms: bool = Field(..., description="Agreement to terms of service")
    agreed_to_privacy: bool = Field(..., description="Agreement to privacy policy")
    marketing_opt_in: bool = Field(default=False, description="Marketing emails opt-in")

    @validator('confirm_password')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v

    @validator('agreed_to_terms')
    def terms_must_be_agreed(cls, v):
        if not v:
            raise ValueError('Must agree to terms of service')
        return v

    @validator('agreed_to_privacy')
    def privacy_must_be_agreed(cls, v):
        if not v:
            raise ValueError('Must agree to privacy policy')
        return v

    @validator('password')
    def validate_password_strength(cls, v):
        """Validate password meets security requirements"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')

        has_upper = any(c.isupper() for c in v)
        has_lower = any(c.islower() for c in v)
        has_digit = any(c.isdigit() for c in v)
        has_special = any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in v)

        if not (has_upper and has_lower and has_digit and has_special):
            raise ValueError('Password must contain uppercase, lowercase, number, and special character')

        return v


class UserLoginRequest(BaseModel):
    """User login request schema"""
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")


class EmailVerificationRequest(BaseModel):
    """Email verification request schema"""
    token: str = Field(..., description="Email verification token")


class ResendVerificationRequest(BaseModel):
    """Resend verification email request schema"""
    email: EmailStr = Field(..., description="User's email address")


# Onboarding Schemas
class AgeVerificationRequest(BaseModel):
    """Age verification request schema"""
    birth_year: int = Field(..., ge=1900, le=2010, description="Year of birth")

    @validator('birth_year')
    def validate_age(cls, v):
        current_year = datetime.now().year
        age = current_year - v
        if age < 18:
            raise ValueError('Must be at least 18 years old')
        if age > 100:
            raise ValueError('Invalid birth year')
        return v


class UserPreferencesRequest(BaseModel):
    """User preferences request schema"""
    target_gender: TargetGender = Field(..., description="Preferred gender to practice with")
    target_age_min: int = Field(..., ge=18, le=100, description="Minimum target age")
    target_age_max: int = Field(..., ge=18, le=100, description="Maximum target age")
    relationship_goal: RelationshipGoal = Field(..., description="Primary relationship goal")

    @validator('target_age_max')
    def validate_age_range(cls, v, values, **kwargs):
        if 'target_age_min' in values and v < values['target_age_min']:
            raise ValueError('Maximum age must be greater than or equal to minimum age')
        return v


class SkillGoalsRequest(BaseModel):
    """Skill goals request schema"""
    primary_skills: List[str] = Field(..., min_items=1, max_items=5, description="Primary skills to develop")
    specific_challenges: List[str] = Field(default=[], max_items=10, description="Specific challenges to work on")
    experience_level: ExperienceLevel = Field(..., description="Current experience level")
    practice_frequency: PracticeFrequency = Field(..., description="Desired practice frequency")

    @validator('primary_skills')
    def validate_primary_skills(cls, v):
        allowed_skills = [
            'conversation_starters',
            'flow_maintenance',
            'storytelling',
            'confidence_building',
            'reading_body_language',
            'humor_and_wit',
            'deep_conversation',
            'flirtation_techniques'
        ]
        for skill in v:
            if skill not in allowed_skills:
                raise ValueError(f'Invalid skill: {skill}. Allowed skills: {", ".join(allowed_skills)}')
        return v


class PrivacySettingsRequest(BaseModel):
    """Privacy settings request schema"""
    notifications_enabled: bool = Field(..., description="Enable notifications")
    analytics_opt_in: bool = Field(default=False, description="Opt-in to analytics")
    privacy_level: PrivacyLevel = Field(default=PrivacyLevel.STANDARD, description="Privacy level")
    marketing_opt_in: bool = Field(default=False, description="Marketing emails opt-in")


class OnboardingProgressRequest(BaseModel):
    """Onboarding progress update schema"""
    step_id: str = Field(..., description="Current step identifier")
    step_data: Optional[Dict[str, Any]] = Field(default=None, description="Step-specific data")
    completed: bool = Field(default=False, description="Whether step is completed")
    skipped: bool = Field(default=False, description="Whether step was skipped")


# Response Schemas
class UserResponse(BaseModel):
    """User response schema"""
    id: str
    email: str
    email_verified: bool
    onboarding_completed: bool
    is_active: bool
    is_premium: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserProfileResponse(BaseModel):
    """User profile response schema"""
    user_id: str
    age_verified: bool
    target_gender: Optional[TargetGender]
    target_age_min: Optional[int]
    target_age_max: Optional[int]
    relationship_goal: Optional[RelationshipGoal]
    primary_skills: List[str]
    specific_challenges: List[str]
    experience_level: Optional[ExperienceLevel]
    practice_frequency: Optional[PracticeFrequency]
    notifications_enabled: Optional[bool]
    analytics_opt_in: bool
    privacy_level: PrivacyLevel
    detected_persona: Optional[DetectedPersona]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserProgressResponse(BaseModel):
    """User progress response schema"""
    user_id: str
    total_conversations: int
    total_practice_time_minutes: int
    current_streak: int
    longest_streak: int
    xp_points: int
    level: int
    achievements_unlocked: List[str]
    confidence_score_average: Optional[int]
    conversation_flow_score_average: Optional[int]
    storytelling_score_average: Optional[int]

    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    """Authentication response schema"""
    success: bool
    user: Optional[UserResponse] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    email_verification_required: bool = False
    message: Optional[str] = None


class OnboardingStepResponse(BaseModel):
    """Individual onboarding step schema"""
    id: str
    title: str
    component: str
    required: bool
    completed: bool
    skippable: bool
    estimated_duration: Optional[int] = None


class OnboardingFlowResponse(BaseModel):
    """Complete onboarding flow response"""
    current_step_index: int
    total_steps: int
    steps: List[OnboardingStepResponse]
    can_go_back: bool
    can_skip_current: bool
    is_complete: bool


class StandardResponse(BaseModel):
    """Standard API response wrapper"""
    success: bool
    data: Optional[Any] = None
    message: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseModel):
    """Error response schema"""
    success: bool = False
    error: Dict[str, Any]
    meta: Optional[Dict[str, Any]] = None


# Validation utility functions
def validate_email_availability(email: str) -> bool:
    """Validate email format and check if available"""
    # This would be implemented to check against database
    # For now, basic format validation is handled by EmailStr
    return True


def validate_password_strength(password: str) -> Dict[str, Any]:
    """Validate password strength and return detailed feedback"""
    score = 0
    feedback = {
        "valid": False,
        "score": 0,
        "requirements": {
            "min_length": len(password) >= 8,
            "has_uppercase": any(c.isupper() for c in password),
            "has_lowercase": any(c.islower() for c in password),
            "has_digit": any(c.isdigit() for c in password),
            "has_special": any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password)
        },
        "suggestions": []
    }

    # Calculate score
    for requirement, met in feedback["requirements"].items():
        if met:
            score += 1

    feedback["score"] = score
    feedback["valid"] = score >= 5

    # Add suggestions
    if not feedback["requirements"]["min_length"]:
        feedback["suggestions"].append("Use at least 8 characters")
    if not feedback["requirements"]["has_uppercase"]:
        feedback["suggestions"].append("Add uppercase letters")
    if not feedback["requirements"]["has_lowercase"]:
        feedback["suggestions"].append("Add lowercase letters")
    if not feedback["requirements"]["has_digit"]:
        feedback["suggestions"].append("Add numbers")
    if not feedback["requirements"]["has_special"]:
        feedback["suggestions"].append("Add special characters (!@#$%^&*)")

    return feedback
"""
Onboarding flow schemas for tracking user onboarding progress.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, Field, validator
from uuid import UUID

from ..models.base import OnboardingStepStatus, PersonaType


class OnboardingSessionCreate(BaseModel):
    """Request schema for creating a new onboarding session."""
    
    device_info: Optional[Dict[str, Any]] = Field(
        None,
        description="Device and platform information"
    )
    referral_source: Optional[str] = Field(
        None,
        max_length=100,
        description="How user arrived at onboarding"
    )
    experiment_variants: Optional[Dict[str, str]] = Field(
        None,
        description="A/B test variants assigned to session"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "device_info": {
                    "platform": "ios",
                    "version": "16.5",
                    "device_model": "iPhone 14"
                },
                "referral_source": "organic",
                "experiment_variants": {
                    "onboarding_flow": "standard",
                    "welcome_message": "benefit_focused"
                }
            }
        }


class OnboardingSessionResponse(BaseModel):
    """Response schema for onboarding session data."""
    
    session_id: UUID = Field(..., description="Onboarding session ID")
    user_id: Optional[UUID] = Field(None, description="Associated user ID if created")
    
    # Progress tracking
    is_completed: bool = Field(..., description="Whether onboarding is completed")
    current_step_index: int = Field(..., description="Current step index (0-based)")
    total_steps: int = Field(..., description="Total number of steps")
    steps_completed: int = Field(..., description="Number of steps completed")
    steps_skipped: int = Field(..., description="Number of steps skipped")
    
    # Timing information
    session_start: datetime = Field(..., description="When session started")
    session_end: Optional[datetime] = Field(None, description="When session ended")
    duration_minutes: Optional[float] = Field(None, description="Session duration in minutes")
    
    # Progress metrics
    completion_rate: float = Field(..., description="Completion percentage")
    skip_rate: float = Field(..., description="Skip percentage")
    
    # Session metadata
    referral_source: Optional[str] = Field(None, description="How user arrived")
    experiment_variants: Dict[str, str] = Field(..., description="A/B test variants")
    
    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
            UUID: lambda uuid: str(uuid)
        }


class OnboardingStepUpdate(BaseModel):
    """Request schema for updating an onboarding step."""
    
    step_id: str = Field(..., max_length=50, description="Step identifier")
    step_name: str = Field(..., max_length=100, description="Human-readable step name")
    step_index: int = Field(..., ge=0, description="Step order in the flow")
    
    # Step data and status
    form_data: Optional[Dict[str, Any]] = Field(
        None,
        description="Data collected in this step"
    )
    status: OnboardingStepStatus = Field(
        OnboardingStepStatus.IN_PROGRESS,
        description="Step status"
    )
    
    # Completion details
    completion_reason: Optional[str] = Field(
        None,
        max_length=50,
        description="Reason for completion"
    )
    skip_reason: Optional[str] = Field(
        None,
        max_length=100,
        description="Reason for skipping if applicable"
    )
    
    # Interaction tracking
    interaction_events: Optional[List[Dict[str, Any]]] = Field(
        None,
        description="User interaction events within this step"
    )
    validation_errors: Optional[List[str]] = Field(
        None,
        description="Validation errors encountered"
    )
    
    class Config:
        use_enum_values = True
        schema_extra = {
            "example": {
                "step_id": "age_verification",
                "step_name": "Age Verification",
                "step_index": 1,  # Step 2 in the 5-screen flow (0-indexed)
                "form_data": {
                    "birth_date": "1998-06-15",
                    "age_verified": True
                },
                "status": "completed",
                "completion_reason": "user_action"
            }
        }


class OnboardingStepResponse(BaseModel):
    """Response schema for onboarding step data."""
    
    step_id: UUID = Field(..., description="Step record ID")
    session_id: UUID = Field(..., description="Parent session ID")
    
    # Step identification
    step_identifier: str = Field(..., description="Step identifier")
    step_name: str = Field(..., description="Step name")
    step_index: int = Field(..., description="Step order")
    
    # Step status and timing
    status: str = Field(..., description="Step status")
    step_started_at: Optional[datetime] = Field(None, description="When step was started")
    step_completed_at: Optional[datetime] = Field(None, description="When step was completed")
    time_spent_minutes: Optional[float] = Field(None, description="Time spent on step in minutes")
    
    # Step data
    form_data: Dict[str, Any] = Field(..., description="Data collected in this step")
    validation_errors: List[str] = Field(..., description="Validation errors")
    attempts_count: int = Field(..., description="Number of attempts")
    
    # Completion details
    completion_reason: Optional[str] = Field(None, description="Reason for completion")
    skip_reason: Optional[str] = Field(None, description="Reason for skipping")
    
    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
            UUID: lambda uuid: str(uuid)
        }


class OnboardingCompleteRequest(BaseModel):
    """Request schema for completing onboarding."""
    
    session_id: UUID = Field(..., description="Onboarding session ID")
    
    # Final collected data for user creation
    registration_data: Dict[str, Any] = Field(
        ...,
        description="Registration form data"
    )
    preferences_data: Dict[str, Any] = Field(
        ...,
        description="User preferences data"
    )
    skill_goals_data: Dict[str, Any] = Field(
        ...,
        description="Skill goals and challenges data"
    )
    
    # Optional completion metadata
    completion_reason: str = Field(
        "user_completed",
        description="Reason for completion"
    )
    final_persona: Optional[PersonaType] = Field(
        None,
        description="Final detected user persona"
    )
    
    @validator('registration_data')
    def validate_registration_data(cls, v):
        required_fields = ['email', 'password', 'birth_date', 'agreed_to_terms', 'agreed_to_privacy']
        for field in required_fields:
            if field not in v:
                raise ValueError(f'registration_data must include {field}')
        return v
    
    @validator('preferences_data')
    def validate_preferences_data(cls, v):
        required_fields = ['target_gender', 'target_age_min', 'target_age_max', 'relationship_goal']
        for field in required_fields:
            if field not in v:
                raise ValueError(f'preferences_data must include {field}')
        return v
    
    class Config:
        use_enum_values = True
        schema_extra = {
            "example": {
                "session_id": "123e4567-e89b-12d3-a456-426614174000",
                "registration_data": {
                    "email": "user@example.com",
                    "password": "SecurePass123!",
                    "birth_date": "1998-06-15",
                    "agreed_to_terms": True,
                    "agreed_to_privacy": True
                },
                "preferences_data": {
                    "target_gender": "everyone",
                    "target_age_min": 22,
                    "target_age_max": 32,
                    "relationship_goal": "dating"
                },
                "skill_goals_data": {
                    "primary_skill_goals": ["conversation_starters", "keeping_flow"],
                    "experience_level": "beginner",
                    "practice_frequency": "weekly",
                    "specific_challenges": []
                },
                "final_persona": "anxious_alex"
            }
        }


class OnboardingProgressResponse(BaseModel):
    """Response schema for onboarding progress tracking."""
    
    session_id: UUID = Field(..., description="Session ID")
    
    # Overall progress
    completion_rate: float = Field(..., description="Overall completion percentage")
    steps_remaining: int = Field(..., description="Number of steps remaining")
    estimated_time_remaining: Optional[int] = Field(
        None,
        description="Estimated time remaining in minutes"
    )
    
    # Current step info
    current_step: Optional[Dict[str, Any]] = Field(
        None,
        description="Current step information"
    )
    next_step: Optional[Dict[str, Any]] = Field(
        None,
        description="Next step information"
    )
    
    # Progress indicators
    can_skip_current: bool = Field(..., description="Whether current step can be skipped")
    can_go_back: bool = Field(..., description="Whether user can go back")
    
    # Analytics data
    time_spent_total: int = Field(..., description="Total time spent in seconds")
    average_step_time: Optional[float] = Field(
        None,
        description="Average time per step in minutes"
    )
    
    class Config:
        json_encoders = {
            UUID: lambda uuid: str(uuid)
        }


class OnboardingAnalyticsResponse(BaseModel):
    """Response schema for onboarding analytics data."""
    
    # Session metrics
    total_sessions: int = Field(..., description="Total number of onboarding sessions")
    completed_sessions: int = Field(..., description="Number of completed sessions")
    abandoned_sessions: int = Field(..., description="Number of abandoned sessions")
    completion_rate: float = Field(..., description="Overall completion rate percentage")
    
    # Timing metrics
    average_completion_time: Optional[float] = Field(
        None,
        description="Average completion time in minutes"
    )
    median_completion_time: Optional[float] = Field(
        None,
        description="Median completion time in minutes"
    )
    
    # Step analytics
    step_completion_rates: Dict[str, float] = Field(
        ...,
        description="Completion rate by step"
    )
    step_skip_rates: Dict[str, float] = Field(
        ...,
        description="Skip rate by step"
    )
    step_average_times: Dict[str, float] = Field(
        ...,
        description="Average time spent per step"
    )
    
    # Drop-off analysis
    common_drop_off_points: List[Dict[str, Any]] = Field(
        ...,
        description="Steps where users commonly abandon"
    )
    
    # User segmentation
    completion_by_persona: Optional[Dict[str, float]] = Field(
        None,
        description="Completion rates by detected persona"
    )
    completion_by_source: Optional[Dict[str, float]] = Field(
        None,
        description="Completion rates by referral source"
    )
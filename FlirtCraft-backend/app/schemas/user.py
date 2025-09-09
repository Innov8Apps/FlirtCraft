"""
User profile and progress schemas.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime, date
from pydantic import BaseModel, Field, validator
from uuid import UUID

from ..models.base import (
    Gender, PremiumTier, PrivacyLevel, ExperienceLevel, 
    PracticeFrequency, RelationshipGoal, PersonaType, SkillGoal
)


class UserProfileResponse(BaseModel):
    """Response schema for user profile data."""
    
    # User identification
    user_id: UUID = Field(..., description="User ID")
    email: str = Field(..., description="User's email address")
    
    # Basic info
    age: int = Field(..., description="User's age")
    is_active: bool = Field(..., description="Whether account is active")
    email_verified: bool = Field(..., description="Whether email is verified")
    onboarding_completed: bool = Field(..., description="Whether onboarding was completed")
    
    # Premium status
    premium_tier: str = Field(..., description="User's premium tier")
    is_premium: bool = Field(..., description="Whether user has active premium")
    premium_expires_at: Optional[datetime] = Field(None, description="Premium expiration date")
    
    # Profile preferences
    target_gender: str = Field(..., description="Target gender preference")
    target_age_min: int = Field(..., description="Minimum age preference")
    target_age_max: int = Field(..., description="Maximum age preference")
    relationship_goal: str = Field(..., description="User's relationship goal")
    
    # Skills and experience
    primary_skills: List[str] = Field(..., description="Primary skills to develop")
    specific_challenges: List[str] = Field(..., description="Specific challenge areas")
    skill_goals: List[str] = Field(..., description="Selected skill goals from onboarding (1-3 goals)")
    experience_level: str = Field(..., description="User's experience level")
    practice_frequency: str = Field(..., description="Desired practice frequency")
    
    # Personalization
    persona_detected: Optional[str] = Field(None, description="Detected user persona")
    privacy_level: str = Field(..., description="User's privacy level")
    
    # Preferences
    notifications_enabled: bool = Field(..., description="Whether notifications are enabled")
    analytics_opt_in: bool = Field(..., description="Whether analytics are enabled")
    marketing_opt_in: bool = Field(..., description="Whether marketing emails are enabled")
    
    # Localization
    timezone: Optional[str] = Field(None, description="User's timezone")
    locale: str = Field(..., description="User's locale")
    
    # Timestamps
    created_at: datetime = Field(..., description="Account creation date")
    updated_at: datetime = Field(..., description="Last profile update")
    onboarding_completed_at: Optional[datetime] = Field(None, description="Onboarding completion date")
    
    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
            UUID: lambda uuid: str(uuid)
        }


class UserProfileUpdate(BaseModel):
    """Request schema for updating user profile."""
    
    # Conversation preferences
    target_gender: Optional[Gender] = Field(None, description="Target gender preference")
    target_age_min: Optional[int] = Field(None, ge=18, le=100, description="Minimum age preference")
    target_age_max: Optional[int] = Field(None, ge=18, le=100, description="Maximum age preference")
    relationship_goal: Optional[RelationshipGoal] = Field(None, description="Relationship goal")
    
    # Skills and experience
    primary_skills: Optional[List[str]] = Field(None, description="Primary skills to develop")
    specific_challenges: Optional[List[str]] = Field(None, description="Specific challenge areas")
    skill_goals: Optional[List[str]] = Field(None, description="Selected skill goals (1-3 goals)")
    experience_level: Optional[ExperienceLevel] = Field(None, description="Experience level")
    practice_frequency: Optional[PracticeFrequency] = Field(None, description="Practice frequency")
    
    # Privacy and preferences
    privacy_level: Optional[PrivacyLevel] = Field(None, description="Privacy level")
    notifications_enabled: Optional[bool] = Field(None, description="Enable notifications")
    analytics_opt_in: Optional[bool] = Field(None, description="Opt into analytics")
    marketing_opt_in: Optional[bool] = Field(None, description="Opt into marketing emails")
    
    # Localization
    timezone: Optional[str] = Field(None, max_length=50, description="Timezone")
    locale: Optional[str] = Field(None, max_length=10, description="Locale")
    
    @validator('target_age_max')
    def valid_age_range(cls, v, values):
        if v is not None and 'target_age_min' in values and values['target_age_min'] is not None:
            if v < values['target_age_min']:
                raise ValueError('target_age_max must be >= target_age_min')
        return v
    
    @validator('skill_goals')
    def validate_skill_goals(cls, v):
        if v is not None:
            if not isinstance(v, list):
                raise ValueError('skill_goals must be a list')
            if len(v) < 1 or len(v) > 3:
                raise ValueError('Must select 1-3 skill goals')
            # Validate that all skill goals are valid enum values
            valid_goals = [goal.value for goal in SkillGoal]
            for goal in v:
                if goal not in valid_goals:
                    raise ValueError(f'Invalid skill goal: {goal}')
        return v
    
    class Config:
        use_enum_values = True


class UserPreferencesUpdate(BaseModel):
    """Request schema for updating user preferences only."""
    
    notifications_enabled: Optional[bool] = Field(None, description="Enable notifications")
    analytics_opt_in: Optional[bool] = Field(None, description="Opt into analytics")
    marketing_opt_in: Optional[bool] = Field(None, description="Opt into marketing emails")
    privacy_level: Optional[PrivacyLevel] = Field(None, description="Privacy level")
    timezone: Optional[str] = Field(None, max_length=50, description="Timezone")
    locale: Optional[str] = Field(None, max_length=10, description="Locale")
    
    class Config:
        use_enum_values = True


class UserProgressResponse(BaseModel):
    """Response schema for user progress and statistics."""
    
    user_id: UUID = Field(..., description="User ID")
    
    # Conversation statistics
    total_conversations: int = Field(..., description="Total conversations completed")
    total_messages_sent: int = Field(..., description="Total messages sent")
    total_practice_time: int = Field(..., description="Total practice time in minutes")
    
    # Streak tracking
    current_streak: int = Field(..., description="Current practice streak")
    longest_streak: int = Field(..., description="Longest practice streak")
    last_practice_date: Optional[date] = Field(None, description="Last practice date")
    
    # XP and leveling
    xp_points: int = Field(..., description="Total XP points")
    level: int = Field(..., description="Current level")
    xp_for_next_level: int = Field(..., description="XP required for next level")
    xp_progress_percent: float = Field(..., description="Progress to next level as percentage")
    
    # Achievement tracking
    achievements_unlocked: List[str] = Field(..., description="List of unlocked achievement IDs")
    total_achievements: int = Field(..., description="Total number of achievements unlocked")
    
    # Performance metrics
    average_confidence_score: Optional[float] = Field(None, description="Average confidence score")
    average_engagement_score: Optional[float] = Field(None, description="Average engagement score")
    average_overall_score: Optional[float] = Field(None, description="Average overall score")
    
    # Progress metadata
    progress_metadata: Dict[str, Any] = Field(..., description="Additional progress data")
    
    # Timestamps
    created_at: datetime = Field(..., description="Progress tracking start date")
    updated_at: datetime = Field(..., description="Last progress update")
    
    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
            date: lambda d: d.isoformat(),
            UUID: lambda uuid: str(uuid)
        }


class UserStatsResponse(BaseModel):
    """Response schema for user statistics and insights."""
    
    user_id: UUID = Field(..., description="User ID")
    
    # Basic stats
    level: int = Field(..., description="Current level")
    xp_points: int = Field(..., description="Total XP points")
    total_conversations: int = Field(..., description="Total conversations")
    current_streak: int = Field(..., description="Current streak")
    
    # Premium status
    is_premium: bool = Field(..., description="Whether user has premium")
    daily_conversations_used: int = Field(..., description="Conversations used today")
    conversation_limit_exceeded: bool = Field(..., description="Whether daily limit exceeded")
    
    # Recent activity
    conversations_this_week: int = Field(..., description="Conversations this week")
    practice_time_this_week: int = Field(..., description="Practice time this week in minutes")
    
    # Performance insights
    improvement_rate: Optional[float] = Field(None, description="Overall improvement rate")
    strongest_skill: Optional[str] = Field(None, description="User's strongest skill area")
    skill_to_work_on: Optional[str] = Field(None, description="Skill area needing work")
    
    # Achievement highlights
    recent_achievements: List[Dict[str, Any]] = Field(..., description="Recently unlocked achievements")
    next_achievement: Optional[Dict[str, Any]] = Field(None, description="Next achievement to unlock")
    
    class Config:
        json_encoders = {
            UUID: lambda uuid: str(uuid)
        }


class UserDashboardResponse(BaseModel):
    """Response schema for user dashboard data."""
    
    # User identification
    user_id: UUID = Field(..., description="User ID")
    email: str = Field(..., description="User's email")
    
    # Quick stats
    level: int = Field(..., description="Current level")
    xp_points: int = Field(..., description="Total XP points")
    current_streak: int = Field(..., description="Current practice streak")
    
    # Today's activity
    conversations_today: int = Field(..., description="Conversations completed today")
    daily_limit_remaining: int = Field(..., description="Remaining daily conversations")
    
    # Recent progress
    recent_conversations: List[Dict[str, Any]] = Field(..., description="Recent conversation summaries")
    recent_achievements: List[Dict[str, Any]] = Field(..., description="Recent achievements")
    
    # Recommendations
    recommended_scenarios: List[Dict[str, Any]] = Field(..., description="Recommended practice scenarios")
    skill_focus_areas: List[str] = Field(..., description="Areas to focus on improving")
    
    # Motivation and engagement
    weekly_goal_progress: float = Field(..., description="Progress toward weekly practice goal")
    encouragement_message: str = Field(..., description="Personalized encouragement message")
    
    class Config:
        json_encoders = {
            UUID: lambda uuid: str(uuid)
        }


class UserSettingsResponse(BaseModel):
    """Response schema for user settings."""
    
    # Notification settings
    notifications_enabled: bool = Field(..., description="Whether notifications are enabled")
    email_notifications: bool = Field(..., description="Whether email notifications are enabled")
    push_notifications: bool = Field(..., description="Whether push notifications are enabled")
    
    # Privacy settings
    privacy_level: str = Field(..., description="Privacy level")
    analytics_opt_in: bool = Field(..., description="Analytics opt-in status")
    marketing_opt_in: bool = Field(..., description="Marketing opt-in status")
    
    # Preferences
    practice_reminders: bool = Field(..., description="Whether practice reminders are enabled")
    achievement_notifications: bool = Field(..., description="Whether achievement notifications are enabled")
    
    # Localization
    timezone: Optional[str] = Field(None, description="User's timezone")
    locale: str = Field(..., description="User's locale")
    
    # Account settings
    email_verified: bool = Field(..., description="Whether email is verified")
    two_factor_enabled: bool = Field(False, description="Whether 2FA is enabled")


class UserSettingsUpdate(BaseModel):
    """Request schema for updating user settings."""
    
    # Notification settings
    notifications_enabled: Optional[bool] = Field(None, description="Enable notifications")
    email_notifications: Optional[bool] = Field(None, description="Enable email notifications")
    push_notifications: Optional[bool] = Field(None, description="Enable push notifications")
    
    # Privacy settings
    privacy_level: Optional[PrivacyLevel] = Field(None, description="Privacy level")
    analytics_opt_in: Optional[bool] = Field(None, description="Opt into analytics")
    marketing_opt_in: Optional[bool] = Field(None, description="Opt into marketing")
    
    # Preferences
    practice_reminders: Optional[bool] = Field(None, description="Enable practice reminders")
    achievement_notifications: Optional[bool] = Field(None, description="Enable achievement notifications")
    
    # Localization
    timezone: Optional[str] = Field(None, max_length=50, description="Timezone")
    locale: Optional[str] = Field(None, max_length=10, description="Locale")
    
    class Config:
        use_enum_values = True


class SkillGoalsUpdate(BaseModel):
    """Request schema for updating user skill goals."""
    
    skill_goals: List[str] = Field(..., description="Selected skill goals (1-3 goals)")
    
    @validator('skill_goals')
    def validate_skill_goals(cls, v):
        if not isinstance(v, list):
            raise ValueError('skill_goals must be a list')
        if len(v) < 1 or len(v) > 3:
            raise ValueError('Must select 1-3 skill goals')
        # Validate that all skill goals are valid enum values
        valid_goals = [goal.value for goal in SkillGoal]
        for goal in v:
            if goal not in valid_goals:
                raise ValueError(f'Invalid skill goal: {goal}')
        return v
    
    class Config:
        use_enum_values = True
        schema_extra = {
            "example": {
                "skill_goals": ["conversation_starters", "maintaining_flow", "storytelling"]
            }
        }
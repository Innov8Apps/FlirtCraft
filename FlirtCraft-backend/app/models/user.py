"""
User models for FlirtCraft onboarding and profile management.
"""

import uuid
from datetime import datetime, date
from typing import List, Optional, Dict, Any
from sqlalchemy import (
    Column, String, Integer, Boolean, Text, DateTime, Date, 
    ForeignKey, CheckConstraint, Index, JSON, Float,
    UniqueConstraint
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID, JSONB, ARRAY
from sqlalchemy.ext.hybrid import hybrid_property

from .base import BaseModel, Gender, PremiumTier, PrivacyLevel, ExperienceLevel, PracticeFrequency, RelationshipGoal, PersonaType, SkillGoal


class User(BaseModel):
    """
    Core user model with authentication and basic profile information.
    Separated from UserProfile to keep auth data lightweight.
    """
    __tablename__ = "users"
    
    # Authentication and identification
    email: Mapped[str] = mapped_column(
        String(255), 
        unique=True, 
        nullable=False, 
        index=True
    )
    
    # Password is handled by Supabase Auth, not stored here
    # We'll store the Supabase user ID for reference
    supabase_user_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        unique=True,
        nullable=True,
        index=True
    )
    
    # Basic demographic info (required for onboarding)
    age: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        info={"description": "User's age for matching preferences"}
    )
    birth_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
        info={"description": "User's birth date for age verification compliance"}
    )
    
    # Premium subscription info
    premium_tier: Mapped[PremiumTier] = mapped_column(
        String(20),
        default=PremiumTier.FREE,
        nullable=False
    )
    premium_expires_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    
    # Usage tracking
    daily_conversations_used: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )
    daily_limit_reset_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    
    # Account status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    onboarding_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    onboarding_completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    
    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    progress = relationship("UserProgress", back_populates="user", uselist=False, cascade="all, delete-orphan") 
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
    onboarding_sessions = relationship("OnboardingSession", back_populates="user", cascade="all, delete-orphan")
    achievements = relationship("UserAchievement", back_populates="user", cascade="all, delete-orphan")
    
    # Constraints
    __table_args__ = (
        CheckConstraint("age >= 18 AND age <= 100", name="valid_age"),
        CheckConstraint("daily_conversations_used >= 0", name="non_negative_conversations"),
        Index("idx_users_email", "email"),
        Index("idx_users_premium", "premium_tier", "premium_expires_at"),
        Index("idx_users_supabase_id", "supabase_user_id"),
    )
    
    @hybrid_property
    def is_premium(self) -> bool:
        """Check if user has active premium subscription."""
        if self.premium_tier != PremiumTier.PREMIUM:
            return False
        if self.premium_expires_at is None:
            return True  # Lifetime premium
        return datetime.now() < self.premium_expires_at
    
    @hybrid_property
    def conversation_limit_exceeded(self) -> bool:
        """Check if user has exceeded daily conversation limit."""
        if self.is_premium:
            return False  # Premium users have unlimited conversations
        
        # Free users get 3 conversations per day
        FREE_DAILY_LIMIT = 3
        return self.daily_conversations_used >= FREE_DAILY_LIMIT
    
    def reset_daily_limit(self):
        """Reset daily conversation counter."""
        self.daily_conversations_used = 0
        self.daily_limit_reset_at = datetime.now()
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, premium={self.is_premium})>"


class UserProfile(BaseModel):
    """
    Detailed user profile with preferences and onboarding data.
    Separated from User to optimize queries and allow for complex profile data.
    """
    __tablename__ = "user_profiles"
    
    # Foreign key to user
    user_id: Mapped[uuid.UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True
    )
    
    # Conversation partner preferences
    target_gender: Mapped[Gender] = mapped_column(
        String(20),
        nullable=False
    )
    target_age_min: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    target_age_max: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    
    # Dating and relationship preferences
    relationship_goal: Mapped[RelationshipGoal] = mapped_column(
        String(30),
        nullable=False
    )
    
    # Skill development goals (stored as JSON array)
    primary_skills: Mapped[List[str]] = mapped_column(
        ARRAY(String),
        default=list,
        nullable=False,
        comment="Primary conversation skills user wants to develop"
    )
    specific_challenges: Mapped[List[str]] = mapped_column(
        ARRAY(String), 
        default=list,
        nullable=False,
        comment="Specific areas user finds challenging"
    )
    skill_goals: Mapped[List[str]] = mapped_column(
        ARRAY(String),
        default=list,
        nullable=False,
        comment="Selected skill goals from onboarding (1-3 goals)"
    )
    
    # Experience and background
    experience_level: Mapped[ExperienceLevel] = mapped_column(
        String(20),
        nullable=False
    )
    practice_frequency: Mapped[PracticeFrequency] = mapped_column(
        String(20),
        nullable=False
    )
    
    # Privacy and preferences  
    privacy_level: Mapped[PrivacyLevel] = mapped_column(
        String(20),
        default=PrivacyLevel.STANDARD,
        nullable=False
    )
    notifications_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )
    analytics_opt_in: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )
    marketing_opt_in: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    
    # Personalization data
    persona_detected: Mapped[Optional[PersonaType]] = mapped_column(
        String(30),
        nullable=True,
        comment="Detected user persona for personalized experience"
    )
    
    # Onboarding metadata (stored as JSON for flexibility)
    onboarding_metadata: Mapped[Dict[str, Any]] = mapped_column(
        JSONB,
        default=dict,
        nullable=False,
        comment="Additional onboarding data and preferences"
    )
    
    # Timezone and localization
    timezone: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True
    )
    locale: Mapped[str] = mapped_column(
        String(10),
        default="en-US",
        nullable=False
    )
    
    # Relationships
    user = relationship("User", back_populates="profile")
    
    # Constraints
    __table_args__ = (
        CheckConstraint("target_age_min >= 18", name="valid_min_age"),
        CheckConstraint("target_age_max <= 100", name="valid_max_age"), 
        CheckConstraint("target_age_min <= target_age_max", name="valid_age_range"),
        Index("idx_user_profiles_user_id", "user_id"),
        Index("idx_user_profiles_preferences", "target_gender", "experience_level"),
    )
    
    def __repr__(self):
        return f"<UserProfile(user_id={self.user_id}, persona={self.persona_detected})>"


class UserProgress(BaseModel):
    """
    User progress tracking and gamification data.
    Separated from User to optimize queries for progress updates.
    """
    __tablename__ = "user_progress"
    
    # Foreign key to user
    user_id: Mapped[uuid.UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True
    )
    
    # Conversation statistics
    total_conversations: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )
    total_messages_sent: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )
    total_practice_time: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="Total practice time in minutes"
    )
    
    # Streak tracking
    current_streak: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )
    longest_streak: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )
    last_practice_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True
    )
    
    # XP and leveling
    xp_points: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )
    level: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False
    )
    
    # Achievement tracking
    achievements_unlocked: Mapped[List[str]] = mapped_column(
        ARRAY(String),
        default=list,
        nullable=False,
        comment="List of achievement IDs unlocked by user"
    )
    
    # Average scores and performance metrics
    average_confidence_score: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
        comment="Average confidence score across conversations"
    )
    average_engagement_score: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
        comment="Average engagement score across conversations"
    )
    average_overall_score: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
        comment="Average overall conversation score"
    )
    
    # Progress metadata
    progress_metadata: Mapped[Dict[str, Any]] = mapped_column(
        JSONB,
        default=dict,
        nullable=False,
        comment="Additional progress tracking data"
    )
    
    # Relationships
    user = relationship("User", back_populates="progress")
    
    # Constraints
    __table_args__ = (
        CheckConstraint("total_conversations >= 0", name="non_negative_conversations"),
        CheckConstraint("total_messages_sent >= 0", name="non_negative_messages"),
        CheckConstraint("total_practice_time >= 0", name="non_negative_practice_time"),
        CheckConstraint("current_streak >= 0", name="non_negative_current_streak"),
        CheckConstraint("longest_streak >= 0", name="non_negative_longest_streak"),
        CheckConstraint("xp_points >= 0", name="non_negative_xp"),
        CheckConstraint("level >= 1", name="minimum_level_one"),
        CheckConstraint("average_confidence_score >= 0 AND average_confidence_score <= 100 OR average_confidence_score IS NULL", name="valid_confidence_score"),
        CheckConstraint("average_engagement_score >= 0 AND average_engagement_score <= 100 OR average_engagement_score IS NULL", name="valid_engagement_score"),
        CheckConstraint("average_overall_score >= 0 AND average_overall_score <= 100 OR average_overall_score IS NULL", name="valid_overall_score"),
        Index("idx_user_progress_user_id", "user_id"),
        Index("idx_user_progress_level_xp", "level", "xp_points"),
    )
    
    @hybrid_property
    def xp_for_next_level(self) -> int:
        """Calculate XP required for next level."""
        # XP required follows formula: level * 1000 + (level - 1) * 500
        # Level 1->2: 1000, Level 2->3: 1500, Level 3->4: 2000, etc.
        next_level = self.level + 1
        return next_level * 1000 + (next_level - 1) * 500
    
    @hybrid_property
    def xp_progress_percent(self) -> float:
        """Calculate percentage progress to next level."""
        current_level_xp = self.level * 1000 + (self.level - 1) * 500
        next_level_xp = self.xp_for_next_level
        level_xp_range = next_level_xp - current_level_xp
        
        if level_xp_range == 0:
            return 100.0
            
        progress = ((self.xp_points - current_level_xp) / level_xp_range) * 100
        return max(0.0, min(100.0, progress))
    
    def add_xp(self, points: int):
        """Add XP points and check for level up."""
        self.xp_points += points
        
        # Check for level up
        while self.xp_points >= self.xp_for_next_level:
            self.level += 1
    
    def update_streak(self, practice_date: date = None):
        """Update practice streak based on practice date."""
        if practice_date is None:
            practice_date = date.today()
        
        if self.last_practice_date is None:
            # First practice session
            self.current_streak = 1
            self.longest_streak = max(self.longest_streak, 1)
        elif (practice_date - self.last_practice_date).days == 1:
            # Consecutive day
            self.current_streak += 1
            self.longest_streak = max(self.longest_streak, self.current_streak)
        elif (practice_date - self.last_practice_date).days > 1:
            # Streak broken
            self.current_streak = 1
        # Same day practice doesn't change streak
        
        self.last_practice_date = practice_date
    
    def __repr__(self):
        return f"<UserProgress(user_id={self.user_id}, level={self.level}, xp={self.xp_points})>"
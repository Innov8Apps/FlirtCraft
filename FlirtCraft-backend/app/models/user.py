"""
User models for FlirtCraft onboarding system
Based on the comprehensive architecture documentation
"""

from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, JSON, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import uuid

from ..core.database import Base


class User(Base):
    """
    Core user model aligned with Supabase Auth
    Minimal data stored here, detailed profile in UserProfile
    """
    __tablename__ = "users"

    # Primary key matching Supabase Auth UUID
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Basic auth info (synced with Supabase)
    email = Column(String(255), unique=True, nullable=False, index=True)
    email_verified = Column(Boolean, default=False)

    # Onboarding status
    onboarding_completed = Column(Boolean, default=False)
    onboarding_completed_at = Column(DateTime(timezone=True), nullable=True)

    # Account status
    is_active = Column(Boolean, default=True)
    is_premium = Column(Boolean, default=False)
    premium_expires_at = Column(DateTime(timezone=True), nullable=True)

    # Usage limits
    daily_conversations_used = Column(Integer, default=0)
    daily_limit_reset_at = Column(DateTime(timezone=True), default=func.now())

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    progress = relationship("UserProgress", back_populates="user", uselist=False, cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, onboarding_completed={self.onboarding_completed})>"


class UserProfile(Base):
    """
    Detailed user profile from onboarding process
    Stores all preference and goal data
    """
    __tablename__ = "user_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)

    # Age verification (required for compliance)
    age_verified = Column(Boolean, default=False, nullable=False)
    birth_year = Column(Integer, nullable=True)  # Store year only for privacy

    # Dating preferences
    target_gender = Column(String(20), nullable=True)
    target_age_min = Column(Integer, nullable=True)
    target_age_max = Column(Integer, nullable=True)
    relationship_goal = Column(String(50), nullable=True)  # dating, relationships, practice, confidence

    # Skill goals and experience
    primary_skills = Column(ARRAY(String), default=[], nullable=False)  # conversation_starters, flow_maintenance, storytelling
    specific_challenges = Column(ARRAY(String), default=[], nullable=False)
    experience_level = Column(String(20), nullable=True)  # beginner, intermediate, returning
    practice_frequency = Column(String(20), nullable=True)  # daily, weekly, occasional

    # Privacy and notification preferences
    notifications_enabled = Column(Boolean, nullable=True)
    analytics_opt_in = Column(Boolean, default=False)
    privacy_level = Column(String(20), default='standard')  # standard, enhanced
    marketing_opt_in = Column(Boolean, default=False)

    # Persona detection (for personalized experience)
    detected_persona = Column(String(50), nullable=True)  # anxiousAlex, comebackCatherine, confidentCarlos, shySarah

    # Onboarding metadata
    onboarding_version = Column(String(10), default='1.0')
    onboarding_duration_seconds = Column(Integer, nullable=True)
    onboarding_steps_completed = Column(ARRAY(String), default=[], nullable=False)
    onboarding_steps_skipped = Column(ARRAY(String), default=[], nullable=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="profile")

    # Check constraints for data integrity
    __table_args__ = (
        CheckConstraint('target_gender IN (\'male\', \'female\', \'everyone\')', name='check_target_gender'),
        CheckConstraint('target_age_min >= 18 AND target_age_min <= 100', name='check_target_age_min'),
        CheckConstraint('target_age_max >= 18 AND target_age_max <= 100', name='check_target_age_max'),
        CheckConstraint('target_age_max >= target_age_min', name='check_age_range_valid'),
        CheckConstraint('relationship_goal IN (\'dating\', \'relationships\', \'practice\', \'confidence\')', name='check_relationship_goal'),
        CheckConstraint('experience_level IN (\'beginner\', \'intermediate\', \'returning\')', name='check_experience_level'),
        CheckConstraint('practice_frequency IN (\'daily\', \'weekly\', \'occasional\')', name='check_practice_frequency'),
        CheckConstraint('privacy_level IN (\'standard\', \'enhanced\')', name='check_privacy_level'),
        CheckConstraint('detected_persona IN (\'anxiousAlex\', \'comebackCatherine\', \'confidentCarlos\', \'shySarah\')', name='check_detected_persona'),
    )

    def __repr__(self):
        return f"<UserProfile(user_id={self.user_id}, experience_level={self.experience_level})>"


class UserProgress(Base):
    """
    User progress tracking and gamification
    Achievements, XP, streaks, etc.
    """
    __tablename__ = "user_progress"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)

    # Conversation statistics
    total_conversations = Column(Integer, default=0)
    total_practice_time_minutes = Column(Integer, default=0)
    successful_conversations = Column(Integer, default=0)  # Based on feedback scores

    # Streaks and engagement
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_practice_date = Column(DateTime(timezone=True), nullable=True)

    # Gamification
    xp_points = Column(Integer, default=0)
    level = Column(Integer, default=1)
    achievements_unlocked = Column(ARRAY(String), default=[], nullable=False)

    # Skill improvement tracking
    confidence_score_average = Column(Integer, nullable=True)  # 0-100
    conversation_flow_score_average = Column(Integer, nullable=True)  # 0-100
    storytelling_score_average = Column(Integer, nullable=True)  # 0-100

    # Weekly/monthly statistics
    weekly_conversations = Column(Integer, default=0)
    monthly_conversations = Column(Integer, default=0)
    weekly_reset_date = Column(DateTime(timezone=True), default=func.now())
    monthly_reset_date = Column(DateTime(timezone=True), default=func.now())

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="progress")

    def __repr__(self):
        return f"<UserProgress(user_id={self.user_id}, level={self.level}, xp={self.xp_points})>"


class Conversation(Base):
    """
    Individual conversation sessions
    """
    __tablename__ = "conversations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Scenario details
    scenario_type = Column(String(50), nullable=False)  # coffee_shop, bookstore, etc.
    difficulty_level = Column(String(10), nullable=False)  # green, yellow, red

    # AI character context (generated for this conversation)
    ai_character_context = Column(JSON, nullable=True)  # appearance, environment, body_language

    # Session details
    status = Column(String(20), default='active')  # active, completed, abandoned
    start_time = Column(DateTime(timezone=True), server_default=func.now())
    end_time = Column(DateTime(timezone=True), nullable=True)
    total_messages = Column(Integer, default=0)

    # Results and feedback
    session_score = Column(Integer, nullable=True)  # 0-100 overall score
    outcome_level = Column(String(10), nullable=True)  # bronze, silver, gold
    feedback_metrics = Column(JSON, nullable=True)  # 6-metric feedback system

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="conversations")
    messages = relationship("ConversationMessage", back_populates="conversation", cascade="all, delete-orphan")

    # Check constraints
    __table_args__ = (
        CheckConstraint('difficulty_level IN (\'green\', \'yellow\', \'red\')', name='check_difficulty_level'),
        CheckConstraint('status IN (\'active\', \'completed\', \'abandoned\')', name='check_status'),
        CheckConstraint('outcome_level IN (\'bronze\', \'silver\', \'gold\')', name='check_outcome_level'),
        CheckConstraint('session_score >= 0 AND session_score <= 100', name='check_session_score'),
    )

    def __repr__(self):
        return f"<Conversation(id={self.id}, scenario={self.scenario_type}, status={self.status})>"


class ConversationMessage(Base):
    """
    Individual messages within conversations
    """
    __tablename__ = "conversation_messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)

    # Message details
    sender_type = Column(String(10), nullable=False)  # user, ai
    content = Column(Text, nullable=False)
    message_order = Column(Integer, nullable=False)

    # AI-specific data
    ai_reasoning = Column(Text, nullable=True)  # AI's reasoning process (if available)
    ai_body_language = Column(String(100), nullable=True)  # AI's described body language
    ai_receptiveness = Column(String(50), nullable=True)  # AI's receptiveness level

    # Real-time feedback (if generated)
    feedback_type = Column(String(20), nullable=True)  # positive, neutral, warning, tip
    feedback_content = Column(Text, nullable=True)
    feedback_score = Column(Integer, nullable=True)  # 1-5 for this specific message

    # Timestamps
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    conversation = relationship("Conversation", back_populates="messages")

    # Check constraints
    __table_args__ = (
        CheckConstraint('sender_type IN (\'user\', \'ai\')', name='check_sender_type'),
        CheckConstraint('feedback_type IN (\'positive\', \'neutral\', \'warning\', \'tip\')', name='check_feedback_type'),
        CheckConstraint('feedback_score >= 1 AND feedback_score <= 5', name='check_feedback_score'),
    )

    def __repr__(self):
        return f"<ConversationMessage(id={self.id}, sender={self.sender_type}, order={self.message_order})>"


class Scenario(Base):
    """
    Available conversation scenarios
    """
    __tablename__ = "scenarios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Scenario identification
    type = Column(String(50), unique=True, nullable=False)  # coffee_shop, bookstore, etc.
    display_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)

    # Availability
    is_premium = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    # Context templates for AI generation
    context_templates = Column(JSON, nullable=False)  # Templates for appearance, environment, etc.
    difficulty_modifiers = Column(JSON, nullable=False)  # Behavior changes per difficulty

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Scenario(type={self.type}, name={self.display_name}, premium={self.is_premium})>"
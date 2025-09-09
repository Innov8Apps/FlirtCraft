"""
FlirtCraft Database Models
==========================
Import all models for the FlirtCraft application.
This file imports models from the organized model packages.
"""

# Import all models from organized packages
from .models.base import (
    Base, TimestampMixin, BaseModel,
    Gender, PremiumTier, DifficultyLevel, ConversationStatus,
    MessageSender, FeedbackType, Outcome, OnboardingStepStatus,
    PrivacyLevel, ExperienceLevel, PracticeFrequency, 
    RelationshipGoal, PersonaType, SkillGoal
)

from .models.user import User, UserProfile, UserProgress
from .models.onboarding import OnboardingSession, OnboardingStep  
from .models.conversation import Conversation, Message, Scenario
from .models.feedback import FeedbackMetrics
from .models.achievement import Achievement, UserAchievement

# Export all models and enums
__all__ = [
    # Base classes and mixins
    "Base",
    "TimestampMixin", 
    "BaseModel",
    
    # Enums
    "Gender",
    "PremiumTier", 
    "DifficultyLevel",
    "ConversationStatus",
    "MessageSender",
    "FeedbackType", 
    "Outcome",
    "OnboardingStepStatus",
    "PrivacyLevel",
    "ExperienceLevel",
    "PracticeFrequency",
    "RelationshipGoal",
    "PersonaType",
    "SkillGoal",
    
    # User models
    "User",
    "UserProfile",
    "UserProgress",
    
    # Onboarding models
    "OnboardingSession",
    "OnboardingStep",
    
    # Conversation models  
    "Conversation",
    "Message",
    "Scenario",
    
    # Feedback models
    "FeedbackMetrics",
    
    # Achievement models
    "Achievement", 
    "UserAchievement"
]
        Integer, 
        nullable=False,
        info={"description": "Maximum age preference for conversation partners"}
    )
    skill_goals: Mapped[List[str]] = mapped_column(
        ARRAY(Text),
        nullable=False,
        default=list,
        info={"description": "List of conversation skills user wants to improve"}
    )
    
    # Premium subscription management
    premium_tier: Mapped[PremiumTier] = mapped_column(
        String(20), 
        nullable=False, 
        default=PremiumTier.FREE,
        index=True
    )
    premium_expires_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), 
        nullable=True,
        info={"description": "Premium subscription expiration date"}
    )
    
    # Daily usage tracking for free tier limitations
    daily_conversations_used: Mapped[int] = mapped_column(
        Integer, 
        nullable=False, 
        default=0,
        info={"description": "Number of conversations used today"}
    )
    daily_limit_reset_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), 
        nullable=True,
        info={"description": "When daily conversation limit resets"}
    )
    
    # Gamification and progress tracking
    xp_points: Mapped[int] = mapped_column(
        Integer, 
        nullable=False, 
        default=0,
        index=True,
        info={"description": "Total experience points earned"}
    )
    level: Mapped[int] = mapped_column(
        Integer, 
        nullable=False, 
        default=1,
        info={"description": "Current user level based on XP"}
    )
    streak_count: Mapped[int] = mapped_column(
        Integer, 
        nullable=False, 
        default=0,
        info={"description": "Current daily conversation streak"}
    )
    streak_updated_at: Mapped[date] = mapped_column(
        Date, 
        nullable=False, 
        default=func.current_date(),
        info={"description": "Last date streak was updated"}
    )
    
    # Metadata
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False, 
        default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False, 
        default=func.now(),
        onupdate=func.now()
    )
    
    # Relationships
    conversations: Mapped[List["Conversation"]] = relationship(
        "Conversation", 
        back_populates="user",
        cascade="all, delete-orphan"
    )
    achievements: Mapped[List["UserAchievement"]] = relationship(
        "UserAchievement", 
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    # Constraints
    __table_args__ = (
        CheckConstraint('age >= 18 AND age <= 100', name='valid_age_range'),
        CheckConstraint('target_age_min >= 18', name='valid_min_age'),
        CheckConstraint('target_age_max <= 100', name='valid_max_age'),
        CheckConstraint('target_age_min <= target_age_max', name='valid_age_range_order'),
        CheckConstraint('daily_conversations_used >= 0', name='non_negative_usage'),
        CheckConstraint('xp_points >= 0', name='non_negative_xp'),
        CheckConstraint('level >= 1', name='positive_level'),
        CheckConstraint('streak_count >= 0', name='non_negative_streak'),
        Index('idx_users_premium_status', 'premium_tier', 'premium_expires_at'),
        Index('idx_users_xp_level', 'xp_points', 'level'),
    )
    
    @hybrid_property
    def is_premium(self) -> bool:
        """Check if user has active premium subscription."""
        if self.premium_tier != PremiumTier.PREMIUM:
            return False
        if self.premium_expires_at is None:
            return True  # Lifetime premium
        return datetime.utcnow() < self.premium_expires_at
    
    @hybrid_property
    def daily_conversations_remaining(self) -> int:
        """Calculate remaining conversations for today (free users only)."""
        if self.is_premium:
            return 999  # Unlimited for premium users
        
        # Reset daily count if needed
        if self.daily_limit_reset_at is None or datetime.utcnow() > self.daily_limit_reset_at:
            return 10 - 0  # Assuming 10 conversations per day for free users
        
        return max(0, 10 - self.daily_conversations_used)

# =============================================================================
# Scenario Management
# =============================================================================

class Scenario(Base):
    """
    Predefined conversation scenarios with difficulty modifiers.
    Includes templates for AI context generation and premium restrictions.
    """
    __tablename__ = "scenarios"
    
    id: Mapped[uuid.UUID] = mapped_column(
        PostgresUUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    type: Mapped[str] = mapped_column(
        String(50), 
        nullable=False, 
        unique=True,
        info={"description": "Unique scenario identifier"}
    )
    display_name: Mapped[str] = mapped_column(
        String(100), 
        nullable=False,
        info={"description": "Human-readable scenario name"}
    )
    description: Mapped[str] = mapped_column(
        Text, 
        nullable=False,
        info={"description": "Detailed scenario description"}
    )
    is_premium: Mapped[bool] = mapped_column(
        Boolean, 
        nullable=False, 
        default=False,
        info={"description": "Whether scenario requires premium subscription"}
    )
    
    # AI context generation templates
    context_templates: Mapped[Dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        info={"description": "Templates for generating AI character context"}
    )
    difficulty_modifiers: Mapped[Dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        info={"description": "Behavior modifications per difficulty level"}
    )
    
    # Metadata
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False, 
        default=func.now()
    )
    
    # Relationships
    conversations: Mapped[List["Conversation"]] = relationship(
        "Conversation", 
        back_populates="scenario"
    )
    
    # Indexes
    __table_args__ = (
        Index('idx_scenarios_type', 'type'),
        Index('idx_scenarios_premium', 'is_premium'),
    )

# =============================================================================
# Conversation Management
# =============================================================================

class Conversation(Base):
    """
    Individual conversation sessions with AI characters.
    Tracks progress, context, and outcomes for analysis and feedback.
    """
    __tablename__ = "conversations"
    
    id: Mapped[uuid.UUID] = mapped_column(
        PostgresUUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4,
        index=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    scenario_type: Mapped[str] = mapped_column(
        String(50),
        ForeignKey("scenarios.type"),
        nullable=False,
        index=True
    )
    difficulty_level: Mapped[DifficultyLevel] = mapped_column(
        String(10), 
        nullable=False,
        info={"description": "Conversation difficulty (green/yellow/red)"}
    )
    
    # AI character context (generated from scenario templates)
    ai_character_context: Mapped[Dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        info={"description": "Generated AI character appearance, environment, body language"}
    )
    
    # Conversation state and progress
    status: Mapped[ConversationStatus] = mapped_column(
        String(20), 
        nullable=False, 
        default=ConversationStatus.ACTIVE,
        index=True
    )
    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False, 
        default=func.now()
    )
    end_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), 
        nullable=True
    )
    total_messages: Mapped[int] = mapped_column(
        Integer, 
        nullable=False, 
        default=0,
        info={"description": "Total number of messages in conversation"}
    )
    
    # Scoring and outcomes
    session_score: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        info={"description": "Overall conversation score (0-100)"}
    )
    outcome: Mapped[Optional[Outcome]] = mapped_column(
        String(20),
        nullable=True,
        info={"description": "Conversation outcome (bronze/silver/gold)"}
    )
    
    # Metadata
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False, 
        default=func.now(),
        index=True
    )
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="conversations")
    scenario: Mapped["Scenario"] = relationship("Scenario", back_populates="conversations")
    messages: Mapped[List["Message"]] = relationship(
        "Message", 
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="Message.message_order"
    )
    feedback_metrics: Mapped[Optional["FeedbackMetrics"]] = relationship(
        "FeedbackMetrics", 
        back_populates="conversation",
        cascade="all, delete-orphan",
        uselist=False
    )
    
    # Constraints
    __table_args__ = (
        CheckConstraint('total_messages >= 0', name='non_negative_messages'),
        CheckConstraint('session_score IS NULL OR (session_score >= 0 AND session_score <= 100)', 
                       name='valid_session_score'),
        CheckConstraint('end_time IS NULL OR end_time >= start_time', name='valid_end_time'),
        Index('idx_conversations_user_status', 'user_id', 'status'),
        Index('idx_conversations_created_at', 'created_at', postgresql_using='btree'),
        Index('idx_conversations_scenario_difficulty', 'scenario_type', 'difficulty_level'),
    )
    
    @hybrid_property
    def duration_minutes(self) -> Optional[float]:
        """Calculate conversation duration in minutes."""
        if self.end_time is None:
            return None
        return (self.end_time - self.start_time).total_seconds() / 60

# =============================================================================
# Message Handling
# =============================================================================

class Message(Base):
    """
    Individual messages within conversations.
    Includes real-time feedback and AI response tracking.
    """
    __tablename__ = "messages"
    
    id: Mapped[uuid.UUID] = mapped_column(
        PostgresUUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    conversation_id: Mapped[uuid.UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    sender_type: Mapped[MessageSender] = mapped_column(
        String(10), 
        nullable=False,
        info={"description": "Whether message is from user or AI"}
    )
    content: Mapped[str] = mapped_column(
        Text, 
        nullable=False,
        info={"description": "Message content"}
    )
    message_order: Mapped[int] = mapped_column(
        Integer, 
        nullable=False,
        info={"description": "Sequential order of message in conversation"}
    )
    
    # Real-time feedback for user messages
    feedback_type: Mapped[Optional[FeedbackType]] = mapped_column(
        String(20),
        nullable=True,
        info={"description": "Type of feedback for this message"}
    )
    feedback_content: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        info={"description": "Specific feedback text for user messages"}
    )
    
    # AI response metadata
    ai_metadata: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        JSONB,
        nullable=True,
        info={"description": "AI response metadata (model used, processing time, etc.)"}
    )
    
    # Timestamp
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False, 
        default=func.now()
    )
    
    # Relationships
    conversation: Mapped["Conversation"] = relationship("Conversation", back_populates="messages")
    
    # Constraints and indexes
    __table_args__ = (
        CheckConstraint('message_order >= 0', name='non_negative_order'),
        UniqueConstraint('conversation_id', 'message_order', name='unique_message_order'),
        Index('idx_messages_conversation_order', 'conversation_id', 'message_order'),
        Index('idx_messages_timestamp', 'timestamp'),
    )

# =============================================================================
# 6-Metric Feedback System
# =============================================================================

class FeedbackMetrics(Base):
    """
    Comprehensive 6-metric feedback system for conversation analysis.
    Provides detailed scoring across different conversation skills.
    """
    __tablename__ = "feedback_metrics"
    
    id: Mapped[uuid.UUID] = mapped_column(
        PostgresUUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    conversation_id: Mapped[uuid.UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True
    )
    
    # Core 6 metrics (0-100 scale)
    engagement_score: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        info={"description": "AI engagement quality and context integration (0-100)"}
    )
    responsiveness_score: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        info={"description": "Active listening and follow-up quality (0-100)"}
    )
    storytelling_score: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        info={"description": "Narrative building and anecdote sharing (0-100)"}
    )
    emotional_intelligence_score: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        info={"description": "Empathy and emotional awareness (0-100)"}
    )
    momentum_score: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        info={"description": "Conversation flow and pacing (0-100)"}
    )
    flirtation_score: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        info={"description": "Creative flirtation (red difficulty only, 0-100)"}
    )
    
    # Computed overall score
    overall_score: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        info={"description": "Computed average of all applicable metrics"}
    )
    
    # Detailed feedback text
    feedback_text: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        info={"description": "Detailed written feedback for the user"}
    )
    
    # Detailed metric breakdowns
    metric_details: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        JSONB,
        nullable=True,
        info={"description": "Detailed breakdown of each metric with specific examples"}
    )
    
    # Metadata
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False, 
        default=func.now()
    )
    
    # Relationships
    conversation: Mapped["Conversation"] = relationship("Conversation", back_populates="feedback_metrics")
    
    # Constraints
    __table_args__ = (
        CheckConstraint('engagement_score IS NULL OR (engagement_score >= 0 AND engagement_score <= 100)', 
                       name='valid_engagement_score'),
        CheckConstraint('responsiveness_score IS NULL OR (responsiveness_score >= 0 AND responsiveness_score <= 100)', 
                       name='valid_responsiveness_score'),
        CheckConstraint('storytelling_score IS NULL OR (storytelling_score >= 0 AND storytelling_score <= 100)', 
                       name='valid_storytelling_score'),
        CheckConstraint('emotional_intelligence_score IS NULL OR (emotional_intelligence_score >= 0 AND emotional_intelligence_score <= 100)', 
                       name='valid_emotional_intelligence_score'),
        CheckConstraint('momentum_score IS NULL OR (momentum_score >= 0 AND momentum_score <= 100)', 
                       name='valid_momentum_score'),
        CheckConstraint('flirtation_score IS NULL OR (flirtation_score >= 0 AND flirtation_score <= 100)', 
                       name='valid_flirtation_score'),
        CheckConstraint('overall_score IS NULL OR (overall_score >= 0 AND overall_score <= 100)', 
                       name='valid_overall_score'),
        Index('idx_feedback_metrics_overall_score', 'overall_score'),
    )

# =============================================================================
# Gamification - Achievements
# =============================================================================

class Achievement(Base):
    """
    Available achievements that users can unlock.
    Defines criteria and rewards for different accomplishments.
    """
    __tablename__ = "achievements"
    
    id: Mapped[uuid.UUID] = mapped_column(
        PostgresUUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    type: Mapped[str] = mapped_column(
        String(50), 
        nullable=False, 
        unique=True,
        info={"description": "Unique achievement identifier"}
    )
    name: Mapped[str] = mapped_column(
        String(100), 
        nullable=False,
        info={"description": "Display name for achievement"}
    )
    description: Mapped[str] = mapped_column(
        Text, 
        nullable=False,
        info={"description": "Achievement description"}
    )
    icon: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        info={"description": "Achievement icon identifier"}
    )
    
    # Requirements and rewards
    requirements: Mapped[Dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        info={"description": "Criteria for unlocking this achievement"}
    )
    xp_reward: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        info={"description": "XP points awarded for earning this achievement"}
    )
    
    # Categorization
    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        info={"description": "Achievement category (conversation, streak, skill, etc.)"}
    )
    difficulty: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="medium",
        info={"description": "Achievement difficulty (easy, medium, hard, legendary)"}
    )
    
    # Metadata
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False, 
        default=func.now()
    )
    
    # Relationships
    user_achievements: Mapped[List["UserAchievement"]] = relationship(
        "UserAchievement", 
        back_populates="achievement"
    )
    
    # Constraints
    __table_args__ = (
        CheckConstraint('xp_reward >= 0', name='non_negative_xp_reward'),
        Index('idx_achievements_category', 'category'),
        Index('idx_achievements_difficulty', 'difficulty'),
    )

class UserAchievement(Base):
    """
    Tracks which achievements users have unlocked and when.
    Links users to their earned achievements with context.
    """
    __tablename__ = "user_achievements"
    
    id: Mapped[uuid.UUID] = mapped_column(
        PostgresUUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    achievement_type: Mapped[str] = mapped_column(
        String(50),
        ForeignKey("achievements.type"),
        nullable=False
    )
    
    # Achievement context
    earned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False, 
        default=func.now()
    )
    conversation_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("conversations.id", ondelete="SET NULL"),
        nullable=True,
        info={"description": "Conversation that triggered this achievement (if applicable)"}
    )
    
    # Additional context
    context_data: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        JSONB,
        nullable=True,
        info={"description": "Additional context about how achievement was earned"}
    )
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="achievements")
    achievement: Mapped["Achievement"] = relationship("Achievement", back_populates="user_achievements")
    conversation: Mapped[Optional["Conversation"]] = relationship("Conversation")
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('user_id', 'achievement_type', name='unique_user_achievement'),
        Index('idx_user_achievements_earned_at', 'earned_at'),
    )

# =============================================================================
# Initialize default data
# =============================================================================

def create_default_scenarios():
    """Create the default 8 scenarios as specified in the architecture."""
    default_scenarios = [
        {
            "type": "coffee_shop",
            "display_name": "Coffee Shops & Cafes",
            "description": "Practice in relaxed cafe environments",
            "is_premium": False,
            "context_templates": {
                "environments": [
                    "Busy morning coffee shop with business professionals",
                    "Quiet afternoon cafe with students and freelancers",
                    "Trendy specialty coffee roastery"
                ],
                "activities": [
                    "Reading a book while sipping coffee",
                    "Working on laptop with headphones nearby",
                    "Waiting in line for their morning latte"
                ]
            },
            "difficulty_modifiers": {
                "green": {"receptiveness": "high", "conversation_starters": 3},
                "yellow": {"receptiveness": "medium", "conversation_starters": 2},
                "red": {"receptiveness": "low", "conversation_starters": 1}
            }
        },
        # Add other scenarios as needed...
    ]
    return default_scenarios

def create_default_achievements():
    """Create default achievements for the gamification system."""
    default_achievements = [
        {
            "type": "ice_breaker",
            "name": "Ice Breaker",
            "description": "Start your first conversation",
            "icon": "ice_cube",
            "requirements": {"conversations_started": 1},
            "xp_reward": 50,
            "category": "conversation",
            "difficulty": "easy"
        },
        {
            "type": "smooth_operator",
            "name": "Smooth Operator",
            "description": "Achieve a gold outcome in a red difficulty conversation",
            "icon": "star_gold",
            "requirements": {"gold_outcomes_red": 1},
            "xp_reward": 500,
            "category": "skill",
            "difficulty": "legendary"
        },
        # Add more achievements as needed...
    ]
    return default_achievements
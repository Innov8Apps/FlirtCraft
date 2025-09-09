"""
Base model classes and common enums for FlirtCraft.
"""

import uuid
from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import Mapped, mapped_column


# Base class for all models
Base = declarative_base()


class TimestampMixin:
    """Mixin to add timestamp fields to models."""
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )


class BaseModel(Base, TimestampMixin):
    """Base model with ID and timestamps."""
    
    __abstract__ = True
    
    id: Mapped[uuid.UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )


# Enums for type safety
class Gender(str, Enum):
    """Gender preferences for conversation partners."""
    MALE = "male"
    FEMALE = "female" 
    RANDOMIZED = "randomized"
    EVERYONE = "everyone"  # Added for inclusive options


class PremiumTier(str, Enum):
    """User premium subscription tiers."""
    FREE = "free"
    PREMIUM = "premium"


class DifficultyLevel(str, Enum):
    """Conversation difficulty levels."""
    GREEN = "green"    # Easy/friendly
    YELLOW = "yellow"  # Medium/neutral
    RED = "red"        # Hard/challenging


class ConversationStatus(str, Enum):
    """Status of conversation sessions."""
    ACTIVE = "active"
    COMPLETED = "completed"
    ABANDONED = "abandoned"
    PAUSED = "paused"


class MessageSender(str, Enum):
    """Type of message sender."""
    USER = "user"
    AI = "ai"


class FeedbackType(str, Enum):
    """Types of feedback for user messages."""
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    WARNING = "warning"
    TIP = "tip"
    ENCOURAGEMENT = "encouragement"


class Outcome(str, Enum):
    """Conversation outcome ratings."""
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"


class OnboardingStepStatus(str, Enum):
    """Status of individual onboarding steps."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SKIPPED = "skipped"


class PrivacyLevel(str, Enum):
    """User privacy preference levels."""
    STANDARD = "standard"
    ENHANCED = "enhanced"


class ExperienceLevel(str, Enum):
    """User experience level with dating/conversations."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    RETURNING = "returning"
    ADVANCED = "advanced"


class PracticeFrequency(str, Enum):
    """How often user wants to practice."""
    DAILY = "daily"
    WEEKLY = "weekly"
    OCCASIONAL = "occasional"
    AS_NEEDED = "as_needed"


class RelationshipGoal(str, Enum):
    """User's relationship goals."""
    DATING = "dating"
    RELATIONSHIPS = "relationships"
    PRACTICE = "practice"
    CONFIDENCE = "confidence"
    SOCIAL_SKILLS = "social_skills"


class PersonaType(str, Enum):
    """Detected user persona types for personalization."""
    ANXIOUS_ALEX = "anxious_alex"
    COMEBACK_CATHERINE = "comeback_catherine"
    CONFIDENT_CARLOS = "confident_carlos"
    SHY_SARAH = "shy_sarah"


class SkillGoal(str, Enum):
    """Skill goals that users can select during onboarding."""
    CONVERSATION_STARTERS = "conversation_starters"
    MAINTAINING_FLOW = "maintaining_flow" 
    STORYTELLING = "storytelling"
    ACTIVE_LISTENING = "active_listening"
    CONFIDENCE_BUILDING = "confidence_building"
    FLIRTING_TECHNIQUES = "flirting_techniques"
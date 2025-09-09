"""
Conversation and scenario models for FlirtCraft.
"""

import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from sqlalchemy import (
    Column, String, Integer, Boolean, Text, DateTime,
    ForeignKey, Index, JSON, CheckConstraint
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID, JSONB
from sqlalchemy.ext.hybrid import hybrid_property

from .base import BaseModel, DifficultyLevel, ConversationStatus, MessageSender, FeedbackType, Outcome


class Scenario(BaseModel):
    """
    Predefined scenarios for conversation practice.
    """
    __tablename__ = "scenarios"
    
    # Scenario identification
    scenario_type: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
        comment="Unique type identifier (e.g., 'coffee_shop')"
    )
    display_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="Human-readable scenario name"
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="Detailed scenario description"
    )
    
    # Scenario configuration
    is_premium: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="Whether this scenario requires premium subscription"
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        comment="Whether this scenario is currently available"
    )
    
    # Scenario templates and configuration
    context_templates: Mapped[Dict[str, Any]] = mapped_column(
        JSONB,
        default=dict,
        nullable=False,
        comment="Templates for AI context generation"
    )
    difficulty_modifiers: Mapped[Dict[str, Any]] = mapped_column(
        JSONB,
        default=dict,
        nullable=False,
        comment="Behavior changes per difficulty level"
    )
    
    # Display and categorization
    category: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="Scenario category for grouping"
    )
    tags: Mapped[list] = mapped_column(
        JSONB,
        default=list,
        nullable=False,
        comment="Tags for scenario filtering and search"
    )
    
    # Ordering and popularity
    sort_order: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="Display order in scenario selection"
    )
    usage_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="Number of times this scenario has been used"
    )
    
    # Relationships
    conversations = relationship("Conversation", back_populates="scenario")
    
    # Constraints
    __table_args__ = (
        Index("idx_scenarios_type", "scenario_type"),
        Index("idx_scenarios_premium_active", "is_premium", "is_active"),
        Index("idx_scenarios_category", "category"),
    )
    
    def __repr__(self):
        return f"<Scenario(type={self.scenario_type}, name={self.display_name})>"


class Conversation(BaseModel):
    """
    Individual conversation practice sessions.
    """
    __tablename__ = "conversations"
    
    # Foreign keys
    user_id: Mapped[uuid.UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    scenario_id: Mapped[uuid.UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("scenarios.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Conversation configuration
    difficulty_level: Mapped[DifficultyLevel] = mapped_column(
        String(10),
        nullable=False
    )
    status: Mapped[ConversationStatus] = mapped_column(
        String(20),
        default=ConversationStatus.ACTIVE,
        nullable=False
    )
    
    # AI character context
    ai_character_context: Mapped[Dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        comment="Generated AI character appearance, environment, and behavior"
    )
    
    # Session timing
    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(),
        nullable=False
    )
    end_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    
    # Conversation metrics
    total_messages: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )
    user_messages_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )
    ai_messages_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )
    
    # Scoring and outcome
    session_score: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="Overall session score 0-100"
    )
    outcome: Mapped[Optional[Outcome]] = mapped_column(
        String(20),
        nullable=True,
        comment="Conversation outcome rating"
    )
    
    # Conversation metadata
    conversation_metadata: Mapped[Dict[str, Any]] = mapped_column(
        JSONB,
        default=dict,
        nullable=False,
        comment="Additional conversation data and settings"
    )
    
    # Relationships
    user = relationship("User", back_populates="conversations")
    scenario = relationship("Scenario", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    feedback_metrics = relationship("FeedbackMetrics", back_populates="conversation", uselist=False, cascade="all, delete-orphan")
    
    # Constraints
    __table_args__ = (
        CheckConstraint("total_messages >= 0", name="non_negative_total_messages"),
        CheckConstraint("user_messages_count >= 0", name="non_negative_user_messages"),
        CheckConstraint("ai_messages_count >= 0", name="non_negative_ai_messages"),
        CheckConstraint("session_score >= 0 AND session_score <= 100 OR session_score IS NULL", name="valid_session_score"),
        CheckConstraint("user_messages_count + ai_messages_count <= total_messages", name="valid_message_counts"),
        Index("idx_conversations_user_id", "user_id"),
        Index("idx_conversations_scenario_id", "scenario_id"),
        Index("idx_conversations_status", "status"),
        Index("idx_conversations_created_at", "created_at"),
        Index("idx_conversations_difficulty", "difficulty_level"),
    )
    
    @hybrid_property
    def duration_minutes(self) -> Optional[float]:
        """Calculate conversation duration in minutes."""
        if not self.end_time:
            # For active conversations, calculate from start to now
            if self.status == ConversationStatus.ACTIVE:
                duration = datetime.now() - self.start_time
                return duration.total_seconds() / 60.0
            return None
        
        duration = self.end_time - self.start_time
        return duration.total_seconds() / 60.0
    
    @hybrid_property
    def is_completed(self) -> bool:
        """Check if conversation is completed."""
        return self.status == ConversationStatus.COMPLETED
    
    @hybrid_property
    def messages_per_minute(self) -> Optional[float]:
        """Calculate average messages per minute."""
        duration = self.duration_minutes
        if duration is None or duration == 0:
            return None
        return self.total_messages / duration
    
    def complete_conversation(self, outcome: Outcome = None, score: int = None):
        """Mark conversation as completed."""
        if self.status != ConversationStatus.COMPLETED:
            self.status = ConversationStatus.COMPLETED
            self.end_time = datetime.now()
            
            if outcome:
                self.outcome = outcome
            if score is not None:
                self.session_score = score
    
    def abandon_conversation(self):
        """Mark conversation as abandoned."""
        if self.status == ConversationStatus.ACTIVE:
            self.status = ConversationStatus.ABANDONED
            self.end_time = datetime.now()
    
    def pause_conversation(self):
        """Pause an active conversation."""
        if self.status == ConversationStatus.ACTIVE:
            self.status = ConversationStatus.PAUSED
    
    def resume_conversation(self):
        """Resume a paused conversation."""
        if self.status == ConversationStatus.PAUSED:
            self.status = ConversationStatus.ACTIVE
    
    def add_message(self, sender: MessageSender):
        """Update message counts when a message is added."""
        self.total_messages += 1
        if sender == MessageSender.USER:
            self.user_messages_count += 1
        elif sender == MessageSender.AI:
            self.ai_messages_count += 1
    
    def __repr__(self):
        return f"<Conversation(id={self.id}, user_id={self.user_id}, status={self.status})>"


class Message(BaseModel):
    """
    Individual messages within conversation sessions.
    """
    __tablename__ = "messages"
    
    # Foreign key
    conversation_id: Mapped[uuid.UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Message identification
    sender_type: Mapped[MessageSender] = mapped_column(
        String(10),
        nullable=False
    )
    message_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Order of message within conversation"
    )
    
    # Message content
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="The actual message text"
    )
    
    # AI-specific data (for AI messages)
    ai_response_data: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        JSONB,
        nullable=True,
        comment="AI response metadata (body language, receptiveness, etc.)"
    )
    
    # Feedback and coaching
    feedback_type: Mapped[Optional[FeedbackType]] = mapped_column(
        String(20),
        nullable=True,
        comment="Type of feedback for user messages"
    )
    feedback_content: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Specific feedback text"
    )
    
    # Message timing
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(),
        nullable=False
    )
    
    # Message metadata
    message_metadata: Mapped[Dict[str, Any]] = mapped_column(
        JSONB,
        default=dict,
        nullable=False,
        comment="Additional message data and analytics"
    )
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
    
    # Constraints
    __table_args__ = (
        CheckConstraint("message_order >= 0", name="non_negative_message_order"),
        CheckConstraint("LENGTH(content) > 0", name="non_empty_content"),
        Index("idx_messages_conversation_id", "conversation_id"),
        Index("idx_messages_order", "conversation_id", "message_order"),
        Index("idx_messages_timestamp", "timestamp"),
        Index("idx_messages_sender", "sender_type"),
        # Ensure unique message order per conversation
        CheckConstraint("(conversation_id, message_order)", name="unique_message_order"),
    )
    
    @hybrid_property
    def is_from_user(self) -> bool:
        """Check if message is from user."""
        return self.sender_type == MessageSender.USER
    
    @hybrid_property
    def is_from_ai(self) -> bool:
        """Check if message is from AI."""
        return self.sender_type == MessageSender.AI
    
    @hybrid_property
    def has_feedback(self) -> bool:
        """Check if message has feedback."""
        return self.feedback_type is not None and self.feedback_content is not None
    
    def add_feedback(self, feedback_type: FeedbackType, content: str):
        """Add feedback to this message."""
        self.feedback_type = feedback_type
        self.feedback_content = content
    
    def clear_feedback(self):
        """Remove feedback from this message."""
        self.feedback_type = None
        self.feedback_content = None
    
    def __repr__(self):
        return f"<Message(id={self.id}, sender={self.sender_type}, order={self.message_order})>"
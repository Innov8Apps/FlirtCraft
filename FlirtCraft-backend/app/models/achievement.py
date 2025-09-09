"""
Achievement and gamification models for FlirtCraft.
"""

import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from sqlalchemy import (
    Column, String, Integer, Boolean, Text, DateTime,
    ForeignKey, Index, JSON, CheckConstraint, Float,
    UniqueConstraint
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID, JSONB
from sqlalchemy.ext.hybrid import hybrid_property

from .base import BaseModel


class Achievement(BaseModel):
    """
    Predefined achievements that users can unlock.
    """
    __tablename__ = "achievements"
    
    # Achievement identification
    achievement_type: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
        comment="Unique achievement identifier"
    )
    
    # Display information
    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="Achievement title displayed to user"
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="Achievement description and requirements"
    )
    
    # Achievement metadata
    category: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        comment="Achievement category (e.g., 'conversation', 'streak', 'skill')"
    )
    difficulty: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        comment="Achievement difficulty level"
    )
    
    # Rewards and progression
    xp_reward: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="XP points awarded for unlocking this achievement"
    )
    badge_icon: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="Icon identifier for the achievement badge"
    )
    
    # Achievement requirements and criteria
    unlock_criteria: Mapped[Dict[str, Any]] = mapped_column(
        JSONB,
        default=dict,
        nullable=False,
        comment="Criteria required to unlock this achievement"
    )
    
    # Display and status
    is_hidden: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="Whether achievement is hidden until unlocked"
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        comment="Whether achievement can currently be earned"
    )
    
    # Statistics
    total_unlocks: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="Number of users who have unlocked this achievement"
    )
    
    # Display order
    sort_order: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="Display order in achievement lists"
    )
    
    # Relationships
    user_achievements = relationship("UserAchievement", back_populates="achievement")
    
    # Constraints
    __table_args__ = (
        CheckConstraint("xp_reward >= 0", name="non_negative_xp_reward"),
        CheckConstraint("total_unlocks >= 0", name="non_negative_unlocks"),
        Index("idx_achievements_type", "achievement_type"),
        Index("idx_achievements_category", "category", "difficulty"),
        Index("idx_achievements_active", "is_active", "is_hidden"),
    )
    
    @hybrid_property
    def unlock_rate(self) -> float:
        """Calculate unlock rate as percentage (would need user count from elsewhere)."""
        # This would need total user count to calculate properly
        # For now, return total unlocks as a proxy
        return float(self.total_unlocks)
    
    def increment_unlocks(self):
        """Increment the total unlock counter."""
        self.total_unlocks += 1
    
    def check_unlock_criteria(self, user_data: Dict[str, Any]) -> bool:
        """
        Check if user meets the unlock criteria for this achievement.
        This would be implemented with specific business logic.
        """
        # Placeholder implementation - would need specific criteria checking
        return True
    
    def __repr__(self):
        return f"<Achievement(type={self.achievement_type}, title={self.title})>"


class UserAchievement(BaseModel):
    """
    Individual achievement unlocks for users.
    """
    __tablename__ = "user_achievements"
    
    # Foreign keys
    user_id: Mapped[uuid.UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    achievement_id: Mapped[uuid.UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("achievements.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )
    
    # Unlock information
    earned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(),
        nullable=False,
        comment="When the achievement was unlocked"
    )
    
    # Context of unlock
    conversation_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("conversations.id", ondelete="SET NULL"),
        nullable=True,
        comment="Conversation that triggered the achievement (if applicable)"
    )
    
    # Achievement progress and metadata
    progress_data: Mapped[Dict[str, Any]] = mapped_column(
        JSONB,
        default=dict,
        nullable=False,
        comment="Data about how the achievement was earned"
    )
    
    # Notification and display status
    is_viewed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="Whether user has seen the achievement notification"
    )
    viewed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="When user viewed the achievement"
    )
    
    # Social features
    is_shared: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="Whether user has shared this achievement"
    )
    shared_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="When achievement was shared"
    )
    
    # Relationships
    user = relationship("User", back_populates="achievements")
    achievement = relationship("Achievement", back_populates="user_achievements")
    conversation = relationship("Conversation", foreign_keys=[conversation_id])
    
    # Constraints
    __table_args__ = (
        # Each user can only unlock each achievement once
        UniqueConstraint("user_id", "achievement_id", name="unique_user_achievement"),
        Index("idx_user_achievements_user_id", "user_id"),
        Index("idx_user_achievements_earned_at", "earned_at"),
        Index("idx_user_achievements_viewed", "is_viewed", "viewed_at"),
    )
    
    def mark_as_viewed(self):
        """Mark achievement as viewed by the user."""
        if not self.is_viewed:
            self.is_viewed = True
            self.viewed_at = datetime.now()
    
    def mark_as_shared(self):
        """Mark achievement as shared by the user."""
        if not self.is_shared:
            self.is_shared = True
            self.shared_at = datetime.now()
    
    @hybrid_property
    def days_since_earned(self) -> int:
        """Calculate days since achievement was earned."""
        delta = datetime.now() - self.earned_at
        return delta.days
    
    def __repr__(self):
        return f"<UserAchievement(user_id={self.user_id}, achievement_id={self.achievement_id})>"
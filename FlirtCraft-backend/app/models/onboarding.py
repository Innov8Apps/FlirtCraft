"""
Onboarding models for FlirtCraft user onboarding flow tracking.
"""

import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from sqlalchemy import (
    Column, String, Integer, Boolean, Text, DateTime,
    ForeignKey, Index, JSON, CheckConstraint
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID, JSONB
from sqlalchemy.ext.hybrid import hybrid_property

from .base import BaseModel, OnboardingStepStatus


class OnboardingSession(BaseModel):
    """
    Tracks a user's onboarding session and overall progress.
    Each user can have multiple onboarding sessions if they restart.
    """
    __tablename__ = "onboarding_sessions"
    
    # Foreign key to user
    user_id: Mapped[uuid.UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Session tracking
    session_start: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(),
        nullable=False
    )
    session_end: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    
    # Progress tracking
    is_completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    current_step_index: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )
    total_steps: Mapped[int] = mapped_column(
        Integer,
        default=5,  # 5-Screen Streamlined Flow
        nullable=False
    )
    
    # Completion statistics
    steps_completed: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )
    steps_skipped: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )
    
    # Analytics data
    device_info: Mapped[Dict[str, Any]] = mapped_column(
        JSONB,
        default=dict,
        nullable=False,
        comment="Device and platform information"
    )
    
    # A/B testing and experiments
    experiment_variants: Mapped[Dict[str, str]] = mapped_column(
        JSONB,
        default=dict,
        nullable=False,
        comment="A/B test variants assigned to this session"
    )
    
    # Session metadata
    referral_source: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="How user arrived at onboarding (organic, referral, campaign, etc.)"
    )
    
    # Form data collected during onboarding (stored temporarily)
    collected_data: Mapped[Dict[str, Any]] = mapped_column(
        JSONB,
        default=dict,
        nullable=False,
        comment="Form data collected during onboarding before user creation"
    )
    
    # Drop-off tracking
    last_active_step: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="Last step user was active on before abandonment"
    )
    abandonment_reason: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="Reason for onboarding abandonment if detected"
    )
    
    # Performance tracking
    total_duration_seconds: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="Total time spent in onboarding session"
    )
    
    # Relationships
    user = relationship("User", back_populates="onboarding_sessions")
    steps = relationship("OnboardingStep", back_populates="session", cascade="all, delete-orphan")
    
    # Constraints
    __table_args__ = (
        CheckConstraint("current_step_index >= 0", name="non_negative_step_index"),
        CheckConstraint("total_steps > 0", name="positive_total_steps"),
        CheckConstraint("steps_completed >= 0", name="non_negative_completed"),
        CheckConstraint("steps_skipped >= 0", name="non_negative_skipped"),
        CheckConstraint("current_step_index <= total_steps", name="step_index_in_range"),
        CheckConstraint("steps_completed <= total_steps", name="completed_in_range"),
        CheckConstraint("steps_skipped <= total_steps", name="skipped_in_range"),
        CheckConstraint("total_duration_seconds >= 0 OR total_duration_seconds IS NULL", name="non_negative_duration"),
        Index("idx_onboarding_sessions_user_id", "user_id"),
        Index("idx_onboarding_sessions_completed", "is_completed", "session_end"),
        Index("idx_onboarding_sessions_progress", "current_step_index", "steps_completed"),
    )
    
    @hybrid_property
    def completion_rate(self) -> float:
        """Calculate completion percentage."""
        if self.total_steps == 0:
            return 0.0
        return (self.steps_completed / self.total_steps) * 100.0
    
    @hybrid_property
    def skip_rate(self) -> float:
        """Calculate skip percentage."""
        if self.total_steps == 0:
            return 0.0
        return (self.steps_skipped / self.total_steps) * 100.0
    
    @hybrid_property
    def duration_minutes(self) -> Optional[float]:
        """Get session duration in minutes."""
        if self.total_duration_seconds is None:
            return None
        return self.total_duration_seconds / 60.0
    
    def mark_completed(self):
        """Mark the onboarding session as completed."""
        if not self.is_completed:
            self.is_completed = True
            self.session_end = datetime.now()
            self.current_step_index = self.total_steps
            
            if self.session_start:
                duration = datetime.now() - self.session_start
                self.total_duration_seconds = int(duration.total_seconds())
    
    def mark_abandoned(self, reason: str = None):
        """Mark the onboarding session as abandoned."""
        if not self.is_completed:
            self.session_end = datetime.now()
            self.abandonment_reason = reason
            
            if self.session_start:
                duration = datetime.now() - self.session_start
                self.total_duration_seconds = int(duration.total_seconds())
    
    def __repr__(self):
        return f"<OnboardingSession(id={self.id}, user_id={self.user_id}, completed={self.is_completed})>"


class OnboardingStep(BaseModel):
    """
    Tracks individual onboarding step completion and metrics.
    Each step in the onboarding flow is recorded separately.
    """
    __tablename__ = "onboarding_steps"
    
    # Foreign key to onboarding session
    session_id: Mapped[uuid.UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("onboarding_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    # Step identification
    step_id: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="Unique identifier for this step type"
    )
    step_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="Human-readable step name"
    )
    step_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Order of this step in the flow"
    )
    
    # Step status and timing
    status: Mapped[OnboardingStepStatus] = mapped_column(
        String(20),
        default=OnboardingStepStatus.PENDING,
        nullable=False
    )
    
    step_started_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    step_completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    
    # Step data and validation
    form_data: Mapped[Dict[str, Any]] = mapped_column(
        JSONB,
        default=dict,
        nullable=False,
        comment="Data collected in this step"
    )
    validation_errors: Mapped[List[str]] = mapped_column(
        JSONB,  # Store as JSON array
        default=list,
        nullable=False,
        comment="Validation errors encountered in this step"
    )
    
    # Step completion metrics
    time_spent_seconds: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="Time spent on this step in seconds"
    )
    attempts_count: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
        comment="Number of times user attempted this step"
    )
    
    # Step-specific metadata
    interaction_events: Mapped[List[Dict[str, Any]]] = mapped_column(
        JSONB,
        default=list,
        nullable=False,
        comment="User interaction events within this step"
    )
    
    # Skip/completion reason
    completion_reason: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="Reason for completion: 'user_action', 'skip', 'timeout', etc."
    )
    skip_reason: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="Reason for skipping if applicable"
    )
    
    # Relationships
    session = relationship("OnboardingSession", back_populates="steps")
    
    # Constraints
    __table_args__ = (
        CheckConstraint("step_index >= 0", name="non_negative_step_index"),
        CheckConstraint("time_spent_seconds >= 0 OR time_spent_seconds IS NULL", name="non_negative_time_spent"),
        CheckConstraint("attempts_count > 0", name="positive_attempts"),
        Index("idx_onboarding_steps_session_id", "session_id"),
        Index("idx_onboarding_steps_step_id", "step_id"),
        Index("idx_onboarding_steps_status", "status", "step_completed_at"),
        Index("idx_onboarding_steps_timing", "step_started_at", "step_completed_at"),
        # Unique constraint to prevent duplicate steps per session
        CheckConstraint("(session_id, step_id)", name="unique_step_per_session"),
    )
    
    @hybrid_property
    def time_spent_minutes(self) -> Optional[float]:
        """Get time spent on step in minutes."""
        if self.time_spent_seconds is None:
            return None
        return self.time_spent_seconds / 60.0
    
    @hybrid_property
    def is_completed(self) -> bool:
        """Check if step is completed."""
        return self.status == OnboardingStepStatus.COMPLETED
    
    @hybrid_property
    def is_skipped(self) -> bool:
        """Check if step was skipped."""
        return self.status == OnboardingStepStatus.SKIPPED
    
    def start_step(self):
        """Mark step as started."""
        if self.status == OnboardingStepStatus.PENDING:
            self.status = OnboardingStepStatus.IN_PROGRESS
            self.step_started_at = datetime.now()
    
    def complete_step(self, form_data: Dict[str, Any] = None, reason: str = "user_action"):
        """Mark step as completed."""
        if self.status != OnboardingStepStatus.COMPLETED:
            self.status = OnboardingStepStatus.COMPLETED
            self.step_completed_at = datetime.now()
            self.completion_reason = reason
            
            if form_data:
                self.form_data.update(form_data)
            
            # Calculate time spent
            if self.step_started_at:
                duration = datetime.now() - self.step_started_at
                self.time_spent_seconds = int(duration.total_seconds())
    
    def skip_step(self, reason: str = "user_choice"):
        """Mark step as skipped."""
        if self.status != OnboardingStepStatus.SKIPPED:
            self.status = OnboardingStepStatus.SKIPPED
            self.step_completed_at = datetime.now()
            self.skip_reason = reason
            self.completion_reason = "skip"
            
            # Calculate time spent if step was started
            if self.step_started_at:
                duration = datetime.now() - self.step_started_at
                self.time_spent_seconds = int(duration.total_seconds())
    
    def add_interaction_event(self, event_type: str, event_data: Dict[str, Any] = None):
        """Add an interaction event to this step."""
        event = {
            "type": event_type,
            "timestamp": datetime.now().isoformat(),
            "data": event_data or {}
        }
        
        # Initialize if not already a list
        if not isinstance(self.interaction_events, list):
            self.interaction_events = []
            
        self.interaction_events.append(event)
    
    def add_validation_error(self, error: str):
        """Add a validation error."""
        if not isinstance(self.validation_errors, list):
            self.validation_errors = []
            
        if error not in self.validation_errors:
            self.validation_errors.append(error)
    
    def clear_validation_errors(self):
        """Clear all validation errors."""
        self.validation_errors = []
    
    def __repr__(self):
        return f"<OnboardingStep(id={self.id}, step_id={self.step_id}, status={self.status})>"
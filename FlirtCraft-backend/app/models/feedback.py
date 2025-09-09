"""
Feedback and evaluation models for FlirtCraft conversations.
"""

import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from sqlalchemy import (
    Column, String, Integer, Boolean, Text, DateTime,
    ForeignKey, Index, JSON, CheckConstraint, Float
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID, JSONB
from sqlalchemy.ext.hybrid import hybrid_property

from .base import BaseModel


class FeedbackMetrics(BaseModel):
    """
    Comprehensive feedback metrics for conversation evaluation.
    Based on the 6-metric feedback system from architecture documentation.
    """
    __tablename__ = "feedback_metrics"
    
    # Foreign key to conversation
    conversation_id: Mapped[uuid.UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,  # One feedback record per conversation
        index=True
    )
    
    # Core 6-metric evaluation scores (0-100)
    engagement_score: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="AI engagement quality and context integration (0-100)"
    )
    responsiveness_score: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="Active listening and follow-up quality (0-100)"
    )
    storytelling_score: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="Narrative building and anecdote sharing (0-100)"
    )
    emotional_intelligence_score: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="Empathy and emotional awareness (0-100)"
    )
    momentum_score: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="Conversation flow and momentum maintenance (0-100)"
    )
    flirtation_score: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="Creative flirtation quality (0-100, Red difficulty only)"
    )
    
    # Calculated overall score
    overall_score: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="Calculated overall conversation score (0-100)"
    )
    
    # Detailed feedback text
    feedback_text: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Detailed written feedback for the user"
    )
    
    # Specific improvement suggestions
    improvement_suggestions: Mapped[list] = mapped_column(
        JSONB,
        default=list,
        nullable=False,
        comment="Specific actionable improvement suggestions"
    )
    
    # Positive highlights
    positive_highlights: Mapped[list] = mapped_column(
        JSONB,
        default=list,
        nullable=False,
        comment="Things the user did well during the conversation"
    )
    
    # Detailed metric breakdown
    metric_breakdown: Mapped[Dict[str, Any]] = mapped_column(
        JSONB,
        default=dict,
        nullable=False,
        comment="Detailed breakdown of each metric with explanations"
    )
    
    # AI evaluation metadata
    evaluation_metadata: Mapped[Dict[str, Any]] = mapped_column(
        JSONB,
        default=dict,
        nullable=False,
        comment="AI evaluation process metadata and confidence scores"
    )
    
    # Generation timestamp
    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(),
        nullable=False,
        comment="When this feedback was generated"
    )
    
    # Quality indicators
    evaluation_confidence: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
        comment="AI confidence in the evaluation (0.0-1.0)"
    )
    human_reviewed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="Whether this feedback was reviewed by a human"
    )
    
    # Relationships
    conversation = relationship("Conversation", back_populates="feedback_metrics")
    
    # Constraints
    __table_args__ = (
        # Score range constraints (0-100)
        CheckConstraint("engagement_score >= 0 AND engagement_score <= 100 OR engagement_score IS NULL", name="valid_engagement_score"),
        CheckConstraint("responsiveness_score >= 0 AND responsiveness_score <= 100 OR responsiveness_score IS NULL", name="valid_responsiveness_score"),
        CheckConstraint("storytelling_score >= 0 AND storytelling_score <= 100 OR storytelling_score IS NULL", name="valid_storytelling_score"),
        CheckConstraint("emotional_intelligence_score >= 0 AND emotional_intelligence_score <= 100 OR emotional_intelligence_score IS NULL", name="valid_emotional_intelligence_score"),
        CheckConstraint("momentum_score >= 0 AND momentum_score <= 100 OR momentum_score IS NULL", name="valid_momentum_score"),
        CheckConstraint("flirtation_score >= 0 AND flirtation_score <= 100 OR flirtation_score IS NULL", name="valid_flirtation_score"),
        CheckConstraint("overall_score >= 0 AND overall_score <= 100 OR overall_score IS NULL", name="valid_overall_score"),
        CheckConstraint("evaluation_confidence >= 0.0 AND evaluation_confidence <= 1.0 OR evaluation_confidence IS NULL", name="valid_confidence"),
        Index("idx_feedback_metrics_conversation", "conversation_id"),
        Index("idx_feedback_metrics_scores", "overall_score", "generated_at"),
        Index("idx_feedback_metrics_human_reviewed", "human_reviewed"),
    )
    
    @hybrid_property
    def has_flirtation_score(self) -> bool:
        """Check if this feedback includes flirtation scoring (Red difficulty)."""
        return self.flirtation_score is not None
    
    @hybrid_property
    def score_count(self) -> int:
        """Count how many individual scores are available."""
        scores = [
            self.engagement_score,
            self.responsiveness_score, 
            self.storytelling_score,
            self.emotional_intelligence_score,
            self.momentum_score,
            self.flirtation_score
        ]
        return sum(1 for score in scores if score is not None)
    
    @hybrid_property
    def average_score(self) -> Optional[float]:
        """Calculate average score from available metrics."""
        scores = [
            self.engagement_score,
            self.responsiveness_score,
            self.storytelling_score, 
            self.emotional_intelligence_score,
            self.momentum_score
        ]
        
        # Add flirtation score if available (Red difficulty only)
        if self.flirtation_score is not None:
            scores.append(self.flirtation_score)
        
        valid_scores = [score for score in scores if score is not None]
        if not valid_scores:
            return None
        
        return sum(valid_scores) / len(valid_scores)
    
    def calculate_overall_score(self):
        """Calculate and set the overall score based on individual metrics."""
        avg_score = self.average_score
        if avg_score is not None:
            self.overall_score = int(round(avg_score))
    
    def get_score_category(self, score: Optional[int]) -> Optional[str]:
        """Get category label for a score."""
        if score is None:
            return None
        
        if score >= 90:
            return "Exceptional"
        elif score >= 80:
            return "Excellent" 
        elif score >= 70:
            return "Good"
        elif score >= 60:
            return "Developing"
        elif score >= 50:
            return "Needs Practice"
        else:
            return "Learning Mode"
    
    @hybrid_property
    def overall_category(self) -> Optional[str]:
        """Get overall performance category."""
        return self.get_score_category(self.overall_score)
    
    def add_improvement_suggestion(self, suggestion: str, category: str = "general"):
        """Add an improvement suggestion."""
        if not isinstance(self.improvement_suggestions, list):
            self.improvement_suggestions = []
        
        self.improvement_suggestions.append({
            "suggestion": suggestion,
            "category": category,
            "timestamp": datetime.now().isoformat()
        })
    
    def add_positive_highlight(self, highlight: str, category: str = "general"):
        """Add a positive highlight."""
        if not isinstance(self.positive_highlights, list):
            self.positive_highlights = []
        
        self.positive_highlights.append({
            "highlight": highlight,
            "category": category,
            "timestamp": datetime.now().isoformat()
        })
    
    def set_metric_breakdown(self, metric: str, score: int, explanation: str, examples: list = None):
        """Set detailed breakdown for a specific metric."""
        if not isinstance(self.metric_breakdown, dict):
            self.metric_breakdown = {}
        
        self.metric_breakdown[metric] = {
            "score": score,
            "explanation": explanation,
            "examples": examples or [],
            "category": self.get_score_category(score)
        }
    
    def is_complete(self) -> bool:
        """Check if feedback evaluation is complete."""
        required_scores = [
            self.engagement_score,
            self.responsiveness_score,
            self.storytelling_score,
            self.emotional_intelligence_score,
            self.momentum_score
        ]
        
        # All base scores must be present
        return all(score is not None for score in required_scores)
    
    def __repr__(self):
        return f"<FeedbackMetrics(conversation_id={self.conversation_id}, overall_score={self.overall_score})>"
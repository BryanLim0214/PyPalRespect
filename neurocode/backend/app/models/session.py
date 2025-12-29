"""
Learning session, exercise, and progress models.
"""
from datetime import datetime, timezone
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Integer, DateTime, ForeignKey, Text, Float, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class Exercise(Base):
    """Python exercise definition."""
    __tablename__ = "exercises"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # Basic info
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)
    difficulty: Mapped[int] = mapped_column(Integer)  # 1-5
    
    # Content
    starter_code: Mapped[str] = mapped_column(Text)
    solution_code: Mapped[str] = mapped_column(Text)
    test_cases: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON
    
    # Categorization
    concept: Mapped[str] = mapped_column(String(50))  # "loops", "variables", etc.
    grade_level: Mapped[int] = mapped_column(Integer)  # 6, 7, or 8
    
    # ADHD-specific
    estimated_minutes: Mapped[int] = mapped_column(Integer, default=10)
    step_count: Mapped[int] = mapped_column(Integer, default=5)
    
    # Personalization tags
    interest_tags: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON
    
    # Steps for micro-task decomposition
    steps: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))


class LearningSession(Base):
    """
    A single learning session (one sitting).
    Used for research analytics on engagement patterns.
    """
    __tablename__ = "learning_sessions"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    exercise_id: Mapped[Optional[int]] = mapped_column(ForeignKey("exercises.id"), nullable=True)
    
    # Timing
    started_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    ended_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Breaks
    break_count: Mapped[int] = mapped_column(Integer, default=0)
    total_break_seconds: Mapped[int] = mapped_column(Integer, default=0)
    
    # Engagement metrics (for research)
    hint_requests: Mapped[int] = mapped_column(Integer, default=0)
    code_runs: Mapped[int] = mapped_column(Integer, default=0)
    errors_encountered: Mapped[int] = mapped_column(Integer, default=0)
    steps_completed: Mapped[int] = mapped_column(Integer, default=0)
    
    # Outcome
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    frustration_events: Mapped[int] = mapped_column(Integer, default=0)
    
    # Relationships
    user: Mapped["User"] = relationship(back_populates="sessions")
    interactions: Mapped[List["TutorInteraction"]] = relationship(back_populates="session")


class TutorInteraction(Base):
    """Individual tutor-student interaction for conversation tracking."""
    __tablename__ = "tutor_interactions"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("learning_sessions.id"))
    
    # Message content
    role: Mapped[str] = mapped_column(String(10))  # "student" or "tutor"
    content: Mapped[str] = mapped_column(Text)
    
    # Context
    current_step: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    code_snapshot: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Timing
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    response_time_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Classification (for research)
    interaction_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    # Relationships
    session: Mapped["LearningSession"] = relationship(back_populates="interactions")


class ExerciseProgress(Base):
    """Student progress on exercises."""
    __tablename__ = "exercise_progress"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    exercise_id: Mapped[int] = mapped_column(ForeignKey("exercises.id"))
    
    # Progress
    current_step: Mapped[int] = mapped_column(Integer, default=1)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Score
    points_earned: Mapped[int] = mapped_column(Integer, default=0)
    hints_used: Mapped[int] = mapped_column(Integer, default=0)
    
    # Code
    last_code: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Timing
    first_started: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    last_updated: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    total_time_seconds: Mapped[int] = mapped_column(Integer, default=0)
    
    # Attempts
    attempt_count: Mapped[int] = mapped_column(Integer, default=1)
    
    # Relationships
    user: Mapped["User"] = relationship(back_populates="progress")

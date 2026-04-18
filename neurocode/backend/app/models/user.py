"""
User and consent models with COPPA compliance fields.
"""
from datetime import datetime, timezone
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Boolean, Integer, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.database import Base

if TYPE_CHECKING:
    from app.models.session import LearningSession, ExerciseProgress


class ADHDProfile(enum.Enum):
    """ADHD presentation types for personalization."""
    PREDOMINANTLY_INATTENTIVE = "inattentive"
    PREDOMINANTLY_HYPERACTIVE = "hyperactive"
    COMBINED = "combined"
    NOT_SPECIFIED = "not_specified"


class UserRole(enum.Enum):
    """Platform user roles."""
    STUDENT = "student"
    TEACHER = "teacher"


class User(Base):
    """
    Platform user (student or teacher).

    COPPA Note: For users under 13, we collect minimal PII and require
    parental consent before any data collection.
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Authentication (minimal PII)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))

    # Role: "student" or "teacher"
    role: Mapped[str] = mapped_column(String(20), default="student", index=True)

    # Teacher-specific (optional)
    display_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    school: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)

    # Age verification (COPPA) - students only; teachers store defaults
    birth_year: Mapped[int] = mapped_column(Integer)
    grade_level: Mapped[int] = mapped_column(Integer)  # 6, 7, or 8 for students
    
    # Consent tracking
    has_parental_consent: Mapped[bool] = mapped_column(Boolean, default=False)
    consent_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    parent_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # ADHD-specific (optional, only with consent)
    adhd_profile: Mapped[Optional[str]] = mapped_column(
        String(50), nullable=True, default="not_specified"
    )
    
    # Preferences (for personalization)
    interests: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    preferred_break_interval: Mapped[int] = mapped_column(Integer, default=20)
    preferred_session_length: Mapped[int] = mapped_column(Integer, default=30)
    
    # Accessibility
    dyslexia_font: Mapped[bool] = mapped_column(Boolean, default=False)
    high_contrast: Mapped[bool] = mapped_column(Boolean, default=False)
    reduce_animations: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Gamification
    total_points: Mapped[int] = mapped_column(Integer, default=0)
    current_streak: Mapped[int] = mapped_column(Integer, default=0)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    last_active: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Relationships
    sessions: Mapped[List["LearningSession"]] = relationship(back_populates="user")
    progress: Mapped[List["ExerciseProgress"]] = relationship(back_populates="user")


class ParentalConsent(Base):
    """
    COPPA-compliant parental consent record.
    
    Stores verification that a parent/guardian has consented to their
    child's participation in the research study and use of the platform.
    """
    __tablename__ = "parental_consents"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    # Parent info (minimal)
    parent_email: Mapped[str] = mapped_column(String(255))
    
    # Consent details
    consent_given: Mapped[bool] = mapped_column(Boolean, default=False)
    consent_timestamp: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    consent_method: Mapped[str] = mapped_column(String(50))  # "email_link", "signed_form"
    consent_ip: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    
    # Research consent (separate from platform consent)
    research_consent: Mapped[bool] = mapped_column(Boolean, default=False)
    data_sharing_consent: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Revocation
    revoked: Mapped[bool] = mapped_column(Boolean, default=False)
    revoked_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

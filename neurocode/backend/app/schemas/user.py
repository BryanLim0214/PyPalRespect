"""
User-related Pydantic schemas.
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime


class UserCreate(BaseModel):
    """Schema for creating a new user."""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    birth_year: int = Field(..., ge=2005, le=2020)
    grade_level: int = Field(..., ge=6, le=8)
    parent_email: Optional[str] = None
    
    @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        if not v.replace('_', '').isalnum():
            raise ValueError('Username must be alphanumeric (underscores allowed)')
        return v.lower()


class RegisterRequest(BaseModel):
    """Registration request with COPPA fields."""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    birth_year: int = Field(..., ge=2005, le=2020)
    grade_level: int = Field(..., ge=6, le=8)
    parent_email: Optional[str] = None
    interests: Optional[List[str]] = None
    
    @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        if not v.replace('_', '').isalnum():
            raise ValueError('Username must be alphanumeric')
        return v.lower()


class ConsentRequest(BaseModel):
    """Parental consent verification request."""
    token: str
    consent_given: bool
    research_consent: bool = False
    data_sharing_consent: bool = False


class UserResponse(BaseModel):
    """User response schema."""
    id: int
    username: str
    grade_level: int
    has_parental_consent: bool
    adhd_profile: Optional[str] = None
    interests: Optional[str] = None
    total_points: int = 0
    current_streak: int = 0
    dyslexia_font: bool = False
    high_contrast: bool = False
    reduce_animations: bool = True
    created_at: datetime
    
    model_config = {"from_attributes": True}


class UserPreferencesUpdate(BaseModel):
    """Schema for updating user preferences."""
    adhd_profile: Optional[str] = None
    interests: Optional[List[str]] = None
    preferred_break_interval: Optional[int] = Field(None, ge=5, le=60)
    preferred_session_length: Optional[int] = Field(None, ge=10, le=90)
    dyslexia_font: Optional[bool] = None
    high_contrast: Optional[bool] = None
    reduce_animations: Optional[bool] = None


class Token(BaseModel):
    """JWT token response."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """JWT token payload data."""
    username: Optional[str] = None
    user_id: Optional[int] = None

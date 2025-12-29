"""
Exercise-related Pydantic schemas.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ExerciseCreate(BaseModel):
    """Schema for creating an exercise."""
    title: str = Field(..., min_length=3, max_length=200)
    description: str
    difficulty: int = Field(..., ge=1, le=5)
    starter_code: str
    solution_code: str
    test_cases: Optional[str] = None  # JSON string
    concept: str = Field(..., max_length=50)
    grade_level: int = Field(..., ge=6, le=8)
    estimated_minutes: int = Field(10, ge=5, le=60)
    step_count: int = Field(5, ge=1, le=10)
    interest_tags: Optional[List[str]] = None
    steps: Optional[str] = None  # JSON string


class ExerciseResponse(BaseModel):
    """Exercise response schema."""
    id: int
    title: str
    description: str
    difficulty: int
    starter_code: str
    concept: str
    grade_level: int
    estimated_minutes: int
    step_count: int
    interest_tags: Optional[str] = None
    steps: Optional[str] = None
    created_at: datetime
    
    model_config = {"from_attributes": True}


class ExerciseProgressResponse(BaseModel):
    """Progress on an exercise."""
    id: int
    exercise_id: int
    current_step: int
    completed: bool
    points_earned: int
    hints_used: int
    last_code: Optional[str] = None
    total_time_seconds: int
    attempt_count: int
    
    model_config = {"from_attributes": True}


class CodeRunRequest(BaseModel):
    """Request to run code."""
    code: str = Field(..., max_length=10000)
    exercise_id: Optional[int] = None


class CodeRunResponse(BaseModel):
    """Response from running code."""
    success: bool
    output: str
    error: Optional[str] = None
    execution_time_ms: int = 0
    test_results: Optional[List[dict]] = None

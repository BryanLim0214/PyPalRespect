"""
Tutor-related Pydantic schemas.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class TutorMessage(BaseModel):
    """Message sent to the tutor."""
    message: str = Field(..., min_length=1, max_length=2000)
    session_id: Optional[int] = None
    current_code: Optional[str] = None
    current_step: Optional[int] = None


class TutorResponse(BaseModel):
    """Response from the tutor."""
    response: str
    is_step: bool = False
    step_number: Optional[int] = None
    total_steps: Optional[int] = None
    suggested_actions: List[str] = []
    celebration: bool = False
    points_earned: int = 0


class HintRequest(BaseModel):
    """Request for a hint."""
    code: str
    error_message: Optional[str] = None
    hint_level: int = Field(1, ge=1, le=4)
    exercise_id: Optional[int] = None


class HintResponse(BaseModel):
    """Hint response from the tutor."""
    hint: str
    hint_level: int
    next_level_available: bool = True


class Step(BaseModel):
    """A single step in task decomposition."""
    number: int
    title: str
    instruction: str
    code_hint: Optional[str] = None
    checkpoint: bool = False


class TaskDecompositionRequest(BaseModel):
    """Request to decompose a task."""
    task: str = Field(..., min_length=5, max_length=500)
    student_interests: List[str] = []


class TaskDecompositionResponse(BaseModel):
    """Task decomposition response."""
    steps: List[Step]
    estimated_time_minutes: int
    celebration_message: str


class ConversationMessage(BaseModel):
    """A message in the conversation history."""
    role: str  # "user" or "model"
    content: str
    timestamp: Optional[datetime] = None

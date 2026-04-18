"""
Exercises API routes.
"""
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import json

from app.database import get_db
from app.models.user import User
from app.models.session import Exercise, ExerciseProgress
from app.schemas.exercise import (
    ExerciseCreate,
    ExerciseResponse,
    ExerciseProgressResponse,
    CodeRunRequest,
    CodeRunResponse,
)
from app.utils.code_runner import run_python_code, run_with_tests
from app.routers.auth import get_current_user

router = APIRouter()


@router.get("/", response_model=List[ExerciseResponse])
async def list_exercises(
    grade_level: Optional[int] = None,
    concept: Optional[str] = None,
    difficulty: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    """List all exercises, with optional filters."""
    query = select(Exercise)
    
    if grade_level:
        query = query.where(Exercise.grade_level == grade_level)
    if concept:
        query = query.where(Exercise.concept == concept)
    if difficulty:
        query = query.where(Exercise.difficulty == difficulty)
    
    result = await db.execute(query.order_by(Exercise.difficulty, Exercise.id))
    exercises = result.scalars().all()
    
    return [ExerciseResponse.model_validate(e) for e in exercises]


@router.get("/{exercise_id}", response_model=ExerciseResponse)
async def get_exercise(
    exercise_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get a specific exercise."""
    exercise = await db.get(Exercise, exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    return ExerciseResponse.model_validate(exercise)


@router.post("/", response_model=ExerciseResponse)
async def create_exercise(
    exercise: ExerciseCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create a new exercise (admin only in production)."""
    new_exercise = Exercise(
        title=exercise.title,
        description=exercise.description,
        difficulty=exercise.difficulty,
        starter_code=exercise.starter_code,
        solution_code=exercise.solution_code,
        test_cases=exercise.test_cases,
        concept=exercise.concept,
        grade_level=exercise.grade_level,
        estimated_minutes=exercise.estimated_minutes,
        step_count=exercise.step_count,
        interest_tags=json.dumps(exercise.interest_tags) if exercise.interest_tags else None,
        steps=exercise.steps,
    )
    
    db.add(new_exercise)
    await db.commit()
    await db.refresh(new_exercise)
    
    return ExerciseResponse.model_validate(new_exercise)


@router.post("/{exercise_id}/run", response_model=CodeRunResponse)
async def run_code(
    exercise_id: int,
    request: CodeRunRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Run code for an exercise."""
    exercise = await db.get(Exercise, exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    # Run the code
    result = run_python_code(request.code)
    
    # Update or create progress
    progress = await _get_or_create_progress(db, current_user.id, exercise_id)
    progress.last_code = request.code
    progress.last_updated = datetime.now(timezone.utc)
    
    await db.commit()
    
    return CodeRunResponse(
        success=result.success,
        output=result.output,
        error=result.error,
        execution_time_ms=result.execution_time_ms,
    )


@router.post("/{exercise_id}/test", response_model=CodeRunResponse)
async def test_code(
    exercise_id: int,
    request: CodeRunRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Test code against exercise test cases."""
    exercise = await db.get(Exercise, exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    if not exercise.test_cases:
        # Just run the code if no tests
        result = run_python_code(request.code)
        return CodeRunResponse(
            success=result.success,
            output=result.output,
            error=result.error,
            execution_time_ms=result.execution_time_ms,
        )
    
    # Parse test cases
    try:
        test_cases = json.loads(exercise.test_cases)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid test cases format")
    
    # Run with tests
    result = run_with_tests(request.code, test_cases)
    
    # Update progress
    progress = await _get_or_create_progress(db, current_user.id, exercise_id)
    progress.last_code = request.code
    progress.last_updated = datetime.now(timezone.utc)
    
    if result.success:
        if not progress.completed:
            progress.completed = True
            progress.completed_at = datetime.now(timezone.utc)
            progress.points_earned = _calculate_points(exercise.difficulty, progress.hints_used)
            current_user.total_points += progress.points_earned
    
    await db.commit()
    
    return CodeRunResponse(
        success=result.success,
        output=result.output,
        error=result.error,
        execution_time_ms=result.execution_time_ms,
        test_results=result.test_results,
    )


@router.get("/{exercise_id}/progress", response_model=ExerciseProgressResponse)
async def get_progress(
    exercise_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get user's progress on an exercise."""
    progress = await _get_or_create_progress(db, current_user.id, exercise_id)
    await db.commit()
    
    return ExerciseProgressResponse.model_validate(progress)


@router.patch("/{exercise_id}/progress")
async def update_progress(
    exercise_id: int,
    step: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update current step in exercise."""
    progress = await _get_or_create_progress(db, current_user.id, exercise_id)
    progress.current_step = step
    progress.last_updated = datetime.now(timezone.utc)
    
    await db.commit()
    
    return {"status": "updated", "current_step": step}


@router.delete("/{exercise_id}/progress")
async def reset_progress(
    exercise_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Reset user's progress on an exercise (start fresh)."""
    # Find existing progress
    result = await db.execute(
        select(ExerciseProgress).where(
            ExerciseProgress.user_id == current_user.id,
            ExerciseProgress.exercise_id == exercise_id,
        )
    )
    progress = result.scalar_one_or_none()
    
    if progress:
        # Reset the progress fields (keep the record for stats)
        progress.current_step = 1
        progress.last_code = None
        progress.hints_used = 0
        progress.completed = False
        progress.completed_at = None
        progress.first_started = datetime.now(timezone.utc)
        progress.last_updated = datetime.now(timezone.utc)
        await db.commit()
        return {"status": "reset", "message": "Progress reset successfully"}
    
    return {"status": "no_progress", "message": "No progress to reset"}


async def _get_or_create_progress(
    db: AsyncSession,
    user_id: int,
    exercise_id: int
) -> ExerciseProgress:
    """Get or create exercise progress record."""
    result = await db.execute(
        select(ExerciseProgress).where(
            ExerciseProgress.user_id == user_id,
            ExerciseProgress.exercise_id == exercise_id,
        )
    )
    progress = result.scalar_one_or_none()
    
    if not progress:
        progress = ExerciseProgress(
            user_id=user_id,
            exercise_id=exercise_id,
            first_started=datetime.now(timezone.utc),
        )
        db.add(progress)
    
    return progress


def _calculate_points(difficulty: int, hints_used: int) -> int:
    """Calculate points based on difficulty and hints used."""
    base_points = difficulty * 20
    hint_penalty = hints_used * 5
    return max(10, base_points - hint_penalty)

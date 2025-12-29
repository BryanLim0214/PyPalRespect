"""
Progress tracking API routes.
"""
from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.user import User
from app.models.session import LearningSession, ExerciseProgress
from app.services.analytics import AnalyticsService
from app.routers.auth import get_current_user

router = APIRouter()


@router.get("/summary")
async def get_progress_summary(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get overall progress summary for the user."""
    analytics = AnalyticsService(db)
    summary = await analytics.get_user_progress_summary(current_user.id)
    
    return {
        **summary,
        "total_points": current_user.total_points,
        "current_streak": current_user.current_streak,
    }


@router.get("/sessions")
async def get_sessions(
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get user's recent learning sessions."""
    result = await db.execute(
        select(LearningSession)
        .where(LearningSession.user_id == current_user.id)
        .order_by(LearningSession.started_at.desc())
        .limit(limit)
    )
    sessions = result.scalars().all()
    
    return [
        {
            "id": s.id,
            "started_at": s.started_at.isoformat(),
            "ended_at": s.ended_at.isoformat() if s.ended_at else None,
            "duration_minutes": (
                (s.ended_at - s.started_at).total_seconds() / 60 
                if s.ended_at else None
            ),
            "completed": s.completed,
            "hint_requests": s.hint_requests,
            "code_runs": s.code_runs,
            "steps_completed": s.steps_completed,
        }
        for s in sessions
    ]


@router.post("/sessions")
async def start_session(
    exercise_id: int = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Start a new learning session."""
    session = LearningSession(
        user_id=current_user.id,
        exercise_id=exercise_id,
        started_at=datetime.now(timezone.utc),
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)
    
    return {"id": session.id, "started_at": session.started_at.isoformat()}


@router.post("/sessions/{session_id}/end")
async def end_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """End a learning session."""
    session = await db.get(LearningSession, session_id)
    
    if not session or session.user_id != current_user.id:
        return {"error": "Session not found"}
    
    session.ended_at = datetime.now(timezone.utc)
    await db.commit()
    
    duration = (session.ended_at - session.started_at).total_seconds() / 60
    
    return {
        "id": session.id,
        "duration_minutes": duration,
        "completed": session.completed,
    }


@router.post("/sessions/{session_id}/break")
async def log_break(
    session_id: int,
    duration_seconds: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Log a break taken during session."""
    session = await db.get(LearningSession, session_id)
    
    if not session or session.user_id != current_user.id:
        return {"error": "Session not found"}
    
    analytics = AnalyticsService(db)
    await analytics.log_session_event(
        session_id, 
        "break_taken", 
        {"duration_seconds": duration_seconds}
    )
    
    return {"status": "logged", "break_count": session.break_count}


@router.get("/exercises")
async def get_exercise_progress_list(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get progress on all exercises the user has attempted."""
    result = await db.execute(
        select(ExerciseProgress)
        .where(ExerciseProgress.user_id == current_user.id)
        .order_by(ExerciseProgress.last_updated.desc())
    )
    progress_list = result.scalars().all()
    
    return [
        {
            "exercise_id": p.exercise_id,
            "current_step": p.current_step,
            "completed": p.completed,
            "points_earned": p.points_earned,
            "hints_used": p.hints_used,
            "attempt_count": p.attempt_count,
            "total_time_seconds": p.total_time_seconds,
        }
        for p in progress_list
    ]


@router.get("/streak")
async def get_streak_info(
    current_user: User = Depends(get_current_user),
):
    """Get user's streak information."""
    return {
        "current_streak": current_user.current_streak,
        "total_points": current_user.total_points,
    }

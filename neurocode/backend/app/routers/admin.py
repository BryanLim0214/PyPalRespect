"""
Admin/researcher API routes for analytics and management.
Updated with seed-exercises update functionality.
"""
from datetime import datetime, timedelta, timezone
from typing import Optional
import sqlalchemy
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.database import get_db
from app.models.user import User
from app.models.session import Exercise, LearningSession, ExerciseProgress
from app.services.analytics import AnalyticsService
from app.routers.auth import require_teacher

router = APIRouter()


@router.get("/analytics")
async def get_analytics(
    days: int = 30,
    _teacher: User = Depends(require_teacher),
    db: AsyncSession = Depends(get_db),
):
    """Get aggregate analytics for research."""
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=days)
    
    analytics = AnalyticsService(db)
    metrics = await analytics.get_aggregate_metrics(start_date, end_date)
    
    return metrics


@router.get("/analytics/engagement")
async def get_engagement_metrics(
    days: int = 7,
    _teacher: User = Depends(require_teacher),
    db: AsyncSession = Depends(get_db),
):
    """Get detailed engagement metrics."""
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=days)
    
    result = await db.execute(
        select(LearningSession).where(
            LearningSession.started_at >= start_date,
            LearningSession.started_at <= end_date,
        )
    )
    sessions = result.scalars().all()
    
    if not sessions:
        return {"message": "No sessions in date range"}
    
    # Group by date
    daily_stats = {}
    for session in sessions:
        date_key = session.started_at.strftime("%Y-%m-%d")
        if date_key not in daily_stats:
            daily_stats[date_key] = {
                "sessions": 0,
                "completed": 0,
                "total_hints": 0,
                "total_frustrations": 0,
                "total_breaks": 0,
            }
        daily_stats[date_key]["sessions"] += 1
        daily_stats[date_key]["completed"] += 1 if session.completed else 0
        daily_stats[date_key]["total_hints"] += session.hint_requests
        daily_stats[date_key]["total_frustrations"] += session.frustration_events
        daily_stats[date_key]["total_breaks"] += session.break_count
    
    return {
        "date_range": {
            "start": start_date.isoformat(),
            "end": end_date.isoformat(),
        },
        "daily_metrics": daily_stats,
    }


@router.get("/users/stats")
async def get_user_stats(
    _teacher: User = Depends(require_teacher),
    db: AsyncSession = Depends(get_db),
):
    """Get aggregate user statistics (anonymized)."""
    # Count users by grade
    result = await db.execute(
        select(User.grade_level, func.count(User.id))
        .group_by(User.grade_level)
    )
    by_grade = {row[0]: row[1] for row in result}
    
    # Count users by ADHD profile
    result = await db.execute(
        select(User.adhd_profile, func.count(User.id))
        .group_by(User.adhd_profile)
    )
    by_profile = {str(row[0] or "not_specified"): row[1] for row in result}
    
    # Total users
    result = await db.execute(select(func.count(User.id)))
    total = result.scalar()
    
    return {
        "total_users": total,
        "by_grade": by_grade,
        "by_adhd_profile": by_profile,
    }


@router.get("/exercises/stats")
async def get_exercise_stats(
    _teacher: User = Depends(require_teacher),
    db: AsyncSession = Depends(get_db),
):
    """Get exercise completion statistics."""
    result = await db.execute(
        select(
            ExerciseProgress.exercise_id,
            func.count(ExerciseProgress.id).label("attempts"),
            func.sum(
                func.cast(ExerciseProgress.completed, type_=sqlalchemy.Integer)
            ).label("completions"),
            func.avg(ExerciseProgress.hints_used).label("avg_hints"),
        )
        .group_by(ExerciseProgress.exercise_id)
    )
    
    stats = []
    for row in result:
        stats.append({
            "exercise_id": row[0],
            "total_attempts": row[1],
            "completions": row[2] or 0,
            "completion_rate": (row[2] or 0) / row[1] if row[1] > 0 else 0,
            "avg_hints_used": float(row[3]) if row[3] else 0,
        })
    
    return {"exercises": stats}


@router.post("/seed-exercises")
async def seed_sample_exercises(
    update_existing: bool = False,
    db: AsyncSession = Depends(get_db),
):
    """
    Seed database with curriculum exercises.
    
    Args:
        update_existing: If True, update existing exercises with new data (steps, code_hints, etc.)
    """
    from app.data.curriculum import get_all_exercises
    
    exercises = get_all_exercises()
    created = 0
    updated = 0
    
    for ex_data in exercises:
        # Check if exercise already exists
        result = await db.execute(
            select(Exercise).where(Exercise.title == ex_data["title"])
        )
        existing = result.scalar_one_or_none()
        
        if existing:
            if update_existing:
                # Update existing exercise with new data
                for key, value in ex_data.items():
                    if key != "title":  # Don't update title
                        setattr(existing, key, value)
                updated += 1
        else:
            exercise = Exercise(**ex_data)
            db.add(exercise)
            created += 1
    
    await db.commit()
    
    return {
        "message": f"Seeded {created} new, updated {updated} existing exercises (total curriculum: {len(exercises)})",
        "created": created,
        "updated": updated
    }

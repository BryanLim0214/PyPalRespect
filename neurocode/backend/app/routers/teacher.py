"""
Teacher-only API routes.

Provides a classroom overview: list of students, per-student progress,
recent activity, and class-wide engagement metrics.
"""
from datetime import datetime, timedelta, timezone
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.session import Exercise, ExerciseProgress, LearningSession
from app.models.user import User
from app.routers.auth import require_teacher

router = APIRouter()


@router.get("/overview")
async def classroom_overview(
    _teacher: User = Depends(require_teacher),
    db: AsyncSession = Depends(get_db),
):
    """High-level stats for the teacher dashboard."""
    total_students_q = await db.execute(
        select(func.count(User.id)).where(User.role == "student")
    )
    total_students = total_students_q.scalar() or 0

    active_cutoff = datetime.now(timezone.utc) - timedelta(days=7)
    active_q = await db.execute(
        select(func.count(User.id)).where(
            User.role == "student",
            User.last_active >= active_cutoff,
        )
    )
    active_students = active_q.scalar() or 0

    exercises_q = await db.execute(select(func.count(Exercise.id)))
    total_exercises = exercises_q.scalar() or 0

    completions_q = await db.execute(
        select(func.count(ExerciseProgress.id)).where(
            ExerciseProgress.completed == True  # noqa: E712
        )
    )
    total_completions = completions_q.scalar() or 0

    return {
        "total_students": total_students,
        "active_last_7_days": active_students,
        "total_exercises": total_exercises,
        "total_completions": total_completions,
    }


@router.get("/students")
async def list_students(
    _teacher: User = Depends(require_teacher),
    db: AsyncSession = Depends(get_db),
):
    """List every student with a compact progress summary."""
    result = await db.execute(
        select(User).where(User.role == "student").order_by(User.username)
    )
    students = result.scalars().all()

    rows = []
    for s in students:
        prog = await db.execute(
            select(ExerciseProgress).where(ExerciseProgress.user_id == s.id)
        )
        progress_list = prog.scalars().all()
        completed = sum(1 for p in progress_list if p.completed)
        attempted = len(progress_list)
        hints = sum(p.hints_used for p in progress_list)

        rows.append({
            "id": s.id,
            "username": s.username,
            "grade_level": s.grade_level,
            "total_points": s.total_points,
            "current_streak": s.current_streak,
            "has_parental_consent": s.has_parental_consent,
            "exercises_attempted": attempted,
            "exercises_completed": completed,
            "hints_used": hints,
            "last_active": s.last_active.isoformat() if s.last_active else None,
            "created_at": s.created_at.isoformat(),
        })

    return rows


@router.get("/students/{student_id}")
async def student_detail(
    student_id: int,
    _teacher: User = Depends(require_teacher),
    db: AsyncSession = Depends(get_db),
):
    """Per-student detail with per-exercise progress and recent sessions."""
    student = await db.get(User, student_id)
    if not student or student.role != "student":
        raise HTTPException(status_code=404, detail="Student not found")

    prog = await db.execute(
        select(ExerciseProgress)
        .where(ExerciseProgress.user_id == student_id)
        .order_by(ExerciseProgress.last_updated.desc())
    )
    progress_rows = prog.scalars().all()

    # Join exercise titles in one pass
    exercise_ids = [p.exercise_id for p in progress_rows]
    ex_map: dict[int, Exercise] = {}
    if exercise_ids:
        ex_q = await db.execute(
            select(Exercise).where(Exercise.id.in_(exercise_ids))
        )
        ex_map = {e.id: e for e in ex_q.scalars().all()}

    exercises = [
        {
            "exercise_id": p.exercise_id,
            "title": ex_map[p.exercise_id].title if p.exercise_id in ex_map else "Unknown",
            "concept": ex_map[p.exercise_id].concept if p.exercise_id in ex_map else None,
            "completed": p.completed,
            "current_step": p.current_step,
            "points_earned": p.points_earned,
            "hints_used": p.hints_used,
            "attempt_count": p.attempt_count,
            "last_updated": p.last_updated.isoformat(),
        }
        for p in progress_rows
    ]

    sess_q = await db.execute(
        select(LearningSession)
        .where(LearningSession.user_id == student_id)
        .order_by(LearningSession.started_at.desc())
        .limit(10)
    )
    sessions = [
        {
            "id": s.id,
            "started_at": s.started_at.isoformat(),
            "ended_at": s.ended_at.isoformat() if s.ended_at else None,
            "completed": s.completed,
            "hint_requests": s.hint_requests,
            "code_runs": s.code_runs,
            "frustration_events": s.frustration_events,
        }
        for s in sess_q.scalars().all()
    ]

    completed_count = sum(1 for p in progress_rows if p.completed)
    hints_used_total = sum(p.hints_used for p in progress_rows)

    return {
        "id": student.id,
        "username": student.username,
        "grade_level": student.grade_level,
        "total_points": student.total_points,
        "current_streak": student.current_streak,
        "has_parental_consent": student.has_parental_consent,
        "exercises_attempted": len(progress_rows),
        "exercises_completed": completed_count,
        "hints_used": hints_used_total,
        "created_at": student.created_at.isoformat(),
        "last_active": student.last_active.isoformat() if student.last_active else None,
        "exercises": exercises,
        "recent_sessions": sessions,
    }


@router.get("/engagement")
async def engagement_trend(
    days: int = 14,
    _teacher: User = Depends(require_teacher),
    db: AsyncSession = Depends(get_db),
):
    """Daily engagement trend for the last N days (class-wide)."""
    start = datetime.now(timezone.utc) - timedelta(days=days)
    result = await db.execute(
        select(LearningSession).where(LearningSession.started_at >= start)
    )
    sessions = result.scalars().all()

    by_day: dict[str, dict] = {}
    for s in sessions:
        key = s.started_at.strftime("%Y-%m-%d")
        day = by_day.setdefault(key, {
            "date": key,
            "sessions": 0,
            "completed": 0,
            "hints": 0,
            "frustrations": 0,
        })
        day["sessions"] += 1
        day["completed"] += 1 if s.completed else 0
        day["hints"] += s.hint_requests
        day["frustrations"] += s.frustration_events

    return {"days": days, "trend": sorted(by_day.values(), key=lambda d: d["date"])}

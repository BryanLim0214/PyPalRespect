"""
Research analytics service for data collection.

All data is anonymized by default. Identifiable data requires
explicit research consent from parent.
"""
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
import logging

from app.models.session import LearningSession, TutorInteraction, ExerciseProgress

logger = logging.getLogger(__name__)


class AnalyticsService:
    """Service for collecting and aggregating research metrics."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def log_session_event(
        self,
        session_id: int,
        event_type: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """
        Log a session event for research analysis.
        
        Events: "hint_requested", "code_run", "error", "step_completed",
                "frustration_expressed", "break_taken", "session_completed"
        
        Returns True if successful.
        """
        try:
            session = await self.db.get(LearningSession, session_id)
            if not session:
                logger.warning(f"Session {session_id} not found")
                return False
            
            if event_type == "hint_requested":
                session.hint_requests += 1
            elif event_type == "code_run":
                session.code_runs += 1
            elif event_type == "error":
                session.errors_encountered += 1
            elif event_type == "step_completed":
                session.steps_completed += 1
            elif event_type == "frustration_expressed":
                session.frustration_events += 1
            elif event_type == "break_taken":
                session.break_count += 1
                if metadata and "duration_seconds" in metadata:
                    session.total_break_seconds += metadata["duration_seconds"]
            elif event_type == "session_completed":
                session.completed = True
                session.ended_at = datetime.now(timezone.utc)
            
            await self.db.commit()
            return True
            
        except Exception as e:
            logger.error(f"Failed to log event: {e}")
            await self.db.rollback()
            return False
    
    async def get_aggregate_metrics(
        self,
        start_date: datetime,
        end_date: datetime,
    ) -> Dict[str, Any]:
        """
        Get aggregate metrics for research reporting.
        All data is anonymized - no individual identification.
        """
        result = await self.db.execute(
            select(LearningSession).where(
                LearningSession.started_at >= start_date,
                LearningSession.started_at <= end_date,
            )
        )
        sessions = result.scalars().all()
        
        if not sessions:
            return {"error": "No data in date range", "total_sessions": 0}
        
        total = len(sessions)
        completed = sum(1 for s in sessions if s.completed)
        
        completed_with_time = [
            s for s in sessions if s.completed and s.ended_at
        ]
        
        avg_duration = 0
        if completed_with_time:
            durations = [
                (s.ended_at - s.started_at).total_seconds() / 60 
                for s in completed_with_time
            ]
            avg_duration = sum(durations) / len(durations)
        
        return {
            "date_range": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat(),
            },
            "total_sessions": total,
            "completed_sessions": completed,
            "completion_rate": completed / total if total > 0 else 0,
            "avg_hints_per_session": sum(s.hint_requests for s in sessions) / total,
            "avg_errors_per_session": sum(s.errors_encountered for s in sessions) / total,
            "avg_breaks_per_session": sum(s.break_count for s in sessions) / total,
            "avg_frustration_events": sum(s.frustration_events for s in sessions) / total,
            "avg_session_duration_minutes": avg_duration,
        }
    
    async def get_user_progress_summary(self, user_id: int) -> Dict[str, Any]:
        """Get progress summary for a specific user (non-identifying)."""
        result = await self.db.execute(
            select(ExerciseProgress).where(ExerciseProgress.user_id == user_id)
        )
        progress_records = result.scalars().all()
        
        if not progress_records:
            return {
                "exercises_attempted": 0,
                "exercises_completed": 0,
                "total_points": 0,
                "total_hints_used": 0,
            }
        
        return {
            "exercises_attempted": len(progress_records),
            "exercises_completed": sum(1 for p in progress_records if p.completed),
            "total_points": sum(p.points_earned for p in progress_records),
            "total_hints_used": sum(p.hints_used for p in progress_records),
            "avg_attempts_per_exercise": sum(p.attempt_count for p in progress_records) / len(progress_records),
        }

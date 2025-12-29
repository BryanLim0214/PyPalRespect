"""
Tests for analytics service.
"""
import pytest
from datetime import datetime, timedelta, timezone


class TestAnalyticsService:
    """Tests for AnalyticsService."""
    
    @pytest.mark.asyncio
    async def test_log_session_event_hint_requested(self, db_session):
        """Test logging hint_requested event."""
        from app.services.analytics import AnalyticsService
        from app.models.user import User
        from app.models.session import LearningSession
        
        # Create user and session
        user = User(
            username="analyticsuser1",
            hashed_password="hashed",
            birth_year=2010,
            grade_level=7,
        )
        db_session.add(user)
        await db_session.commit()
        
        session = LearningSession(user_id=user.id)
        db_session.add(session)
        await db_session.commit()
        
        # Log event
        analytics = AnalyticsService(db_session)
        result = await analytics.log_session_event(session.id, "hint_requested")
        
        assert result == True
        await db_session.refresh(session)
        assert session.hint_requests == 1
    
    @pytest.mark.asyncio
    async def test_log_session_event_code_run(self, db_session):
        """Test logging code_run event."""
        from app.services.analytics import AnalyticsService
        from app.models.user import User
        from app.models.session import LearningSession
        
        user = User(
            username="analyticsuser2",
            hashed_password="hashed",
            birth_year=2010,
            grade_level=7,
        )
        db_session.add(user)
        await db_session.commit()
        
        session = LearningSession(user_id=user.id)
        db_session.add(session)
        await db_session.commit()
        
        analytics = AnalyticsService(db_session)
        await analytics.log_session_event(session.id, "code_run")
        await analytics.log_session_event(session.id, "code_run")
        await analytics.log_session_event(session.id, "code_run")
        
        await db_session.refresh(session)
        assert session.code_runs == 3
    
    @pytest.mark.asyncio
    async def test_log_session_event_frustration(self, db_session):
        """Test logging frustration_expressed event."""
        from app.services.analytics import AnalyticsService
        from app.models.user import User
        from app.models.session import LearningSession
        
        user = User(
            username="analyticsuser3",
            hashed_password="hashed",
            birth_year=2010,
            grade_level=7,
        )
        db_session.add(user)
        await db_session.commit()
        
        session = LearningSession(user_id=user.id)
        db_session.add(session)
        await db_session.commit()
        
        analytics = AnalyticsService(db_session)
        await analytics.log_session_event(session.id, "frustration_expressed")
        
        await db_session.refresh(session)
        assert session.frustration_events == 1
    
    @pytest.mark.asyncio
    async def test_log_session_event_break_taken(self, db_session):
        """Test logging break_taken event with duration."""
        from app.services.analytics import AnalyticsService
        from app.models.user import User
        from app.models.session import LearningSession
        
        user = User(
            username="analyticsuser4",
            hashed_password="hashed",
            birth_year=2010,
            grade_level=7,
        )
        db_session.add(user)
        await db_session.commit()
        
        session = LearningSession(user_id=user.id)
        db_session.add(session)
        await db_session.commit()
        
        analytics = AnalyticsService(db_session)
        await analytics.log_session_event(
            session.id, 
            "break_taken",
            {"duration_seconds": 300}
        )
        
        await db_session.refresh(session)
        assert session.break_count == 1
        assert session.total_break_seconds == 300
    
    @pytest.mark.asyncio
    async def test_log_session_event_session_completed(self, db_session):
        """Test logging session_completed event."""
        from app.services.analytics import AnalyticsService
        from app.models.user import User
        from app.models.session import LearningSession
        
        user = User(
            username="analyticsuser5",
            hashed_password="hashed",
            birth_year=2010,
            grade_level=7,
        )
        db_session.add(user)
        await db_session.commit()
        
        session = LearningSession(user_id=user.id)
        db_session.add(session)
        await db_session.commit()
        
        analytics = AnalyticsService(db_session)
        await analytics.log_session_event(session.id, "session_completed")
        
        await db_session.refresh(session)
        assert session.completed == True
        assert session.ended_at is not None
    
    @pytest.mark.asyncio
    async def test_log_session_event_invalid_session(self, db_session):
        """Test logging event for non-existent session."""
        from app.services.analytics import AnalyticsService
        
        analytics = AnalyticsService(db_session)
        result = await analytics.log_session_event(99999, "hint_requested")
        
        assert result == False
    
    @pytest.mark.asyncio
    async def test_get_aggregate_metrics(self, db_session):
        """Test getting aggregate metrics."""
        from app.services.analytics import AnalyticsService
        from app.models.user import User
        from app.models.session import LearningSession
        
        user = User(
            username="metricsuser_analytics",
            hashed_password="hashed",
            birth_year=2010,
            grade_level=7,
        )
        db_session.add(user)
        await db_session.commit()
        
        # Create sessions
        for i in range(3):
            session = LearningSession(
                user_id=user.id,
                started_at=datetime.now(timezone.utc) - timedelta(hours=i),
                hint_requests=i,
                code_runs=i * 2,
            )
            db_session.add(session)
        await db_session.commit()
        
        # Mark one as completed
        session.completed = True
        session.ended_at = datetime.now(timezone.utc)
        await db_session.commit()
        
        analytics = AnalyticsService(db_session)
        metrics = await analytics.get_aggregate_metrics(
            datetime.now(timezone.utc) - timedelta(days=1),
            datetime.now(timezone.utc) + timedelta(hours=1)
        )
        
        assert metrics["total_sessions"] >= 3  # At least our 3 sessions
        assert "completion_rate" in metrics
        assert "avg_hints_per_session" in metrics
    
    @pytest.mark.asyncio
    async def test_get_aggregate_metrics_empty_range(self, db_session):
        """Test getting metrics with no data in range."""
        from app.services.analytics import AnalyticsService
        
        analytics = AnalyticsService(db_session)
        metrics = await analytics.get_aggregate_metrics(
            datetime.now(timezone.utc) + timedelta(days=100),
            datetime.now(timezone.utc) + timedelta(days=101)
        )
        
        assert metrics["total_sessions"] == 0
        assert "error" in metrics
    
    @pytest.mark.asyncio
    async def test_get_user_progress_summary(self, db_session):
        """Test getting user progress summary."""
        from app.services.analytics import AnalyticsService
        from app.models.user import User
        from app.models.session import Exercise, ExerciseProgress
        
        user = User(
            username="progresssummaryuser",
            hashed_password="hashed",
            birth_year=2010,
            grade_level=7,
        )
        exercise = Exercise(
            title="Test",
            description="Test",
            difficulty=1,
            starter_code="",
            solution_code="",
            concept="print",
            grade_level=7,
        )
        db_session.add(user)
        db_session.add(exercise)
        await db_session.commit()
        
        progress = ExerciseProgress(
            user_id=user.id,
            exercise_id=exercise.id,
            completed=True,
            points_earned=20,
            hints_used=2,
        )
        db_session.add(progress)
        await db_session.commit()
        
        analytics = AnalyticsService(db_session)
        summary = await analytics.get_user_progress_summary(user.id)
        
        assert summary["exercises_attempted"] == 1
        assert summary["exercises_completed"] == 1
        assert summary["total_points"] == 20
        assert summary["total_hints_used"] == 2
    
    @pytest.mark.asyncio
    async def test_get_user_progress_summary_empty(self, db_session):
        """Test getting progress summary for user with no progress."""
        from app.services.analytics import AnalyticsService
        
        analytics = AnalyticsService(db_session)
        summary = await analytics.get_user_progress_summary(99999)
        
        assert summary["exercises_attempted"] == 0
        assert summary["exercises_completed"] == 0

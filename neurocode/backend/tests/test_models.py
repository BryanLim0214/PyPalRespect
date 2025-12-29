"""
Tests for database models.
"""
import pytest
from datetime import datetime, timezone


class TestUserModel:
    """Tests for User model."""
    
    @pytest.mark.asyncio
    async def test_user_creation(self, db_session):
        """Test creating a user."""
        from app.models.user import User
        
        user = User(
            username="testuser",
            hashed_password="hashed123",
            birth_year=2010,
            grade_level=7,
            has_parental_consent=False,
        )
        
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        
        assert user.id is not None
        assert user.username == "testuser"
        assert user.grade_level == 7
        assert user.has_parental_consent == False
    
    @pytest.mark.asyncio
    async def test_user_default_values(self, db_session):
        """Test user default values are set correctly."""
        from app.models.user import User
        
        user = User(
            username="defaultsuser",
            hashed_password="hashed",
            birth_year=2011,
            grade_level=6,
        )
        
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        
        # Check defaults
        assert user.reduce_animations == True  # ADHD-friendly default
        assert user.dyslexia_font == False
        assert user.high_contrast == False
        assert user.total_points == 0
        assert user.current_streak == 0
        assert user.preferred_break_interval == 20
        assert user.preferred_session_length == 30
    
    @pytest.mark.asyncio
    async def test_user_adhd_profile(self, db_session):
        """Test ADHD profile storage."""
        from app.models.user import User
        
        user = User(
            username="adhduser",
            hashed_password="hashed",
            birth_year=2010,
            grade_level=7,
            adhd_profile="combined",
        )
        
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        
        assert user.adhd_profile == "combined"


class TestParentalConsentModel:
    """Tests for ParentalConsent model."""
    
    @pytest.mark.asyncio
    async def test_consent_creation(self, db_session):
        """Test creating parental consent record."""
        from app.models.user import User, ParentalConsent
        
        # Create user first
        user = User(
            username="childuser",
            hashed_password="hashed",
            birth_year=2013,
            grade_level=6,
            parent_email="parent@test.com",
        )
        db_session.add(user)
        await db_session.commit()
        
        # Create consent
        consent = ParentalConsent(
            user_id=user.id,
            parent_email="parent@test.com",
            consent_given=True,
            consent_method="email_link",
            research_consent=True,
            data_sharing_consent=False,
        )
        
        db_session.add(consent)
        await db_session.commit()
        await db_session.refresh(consent)
        
        assert consent.id is not None
        assert consent.consent_given == True
        assert consent.research_consent == True
        assert consent.data_sharing_consent == False
        assert consent.revoked == False


class TestExerciseModel:
    """Tests for Exercise model."""
    
    @pytest.mark.asyncio
    async def test_exercise_creation(self, db_session):
        """Test creating an exercise."""
        from app.models.session import Exercise
        
        exercise = Exercise(
            title="Test Exercise",
            description="A test exercise",
            difficulty=2,
            starter_code="# Start here",
            solution_code='print("done")',
            concept="variables",
            grade_level=6,
            estimated_minutes=10,
            step_count=3,
        )
        
        db_session.add(exercise)
        await db_session.commit()
        await db_session.refresh(exercise)
        
        assert exercise.id is not None
        assert exercise.title == "Test Exercise"
        assert exercise.difficulty == 2


class TestLearningSessionModel:
    """Tests for LearningSession model."""
    
    @pytest.mark.asyncio
    async def test_session_creation(self, db_session):
        """Test creating a learning session."""
        from app.models.user import User
        from app.models.session import LearningSession
        
        # Create user
        user = User(
            username="sessionuser",
            hashed_password="hashed",
            birth_year=2010,
            grade_level=7,
        )
        db_session.add(user)
        await db_session.commit()
        
        # Create session
        session = LearningSession(
            user_id=user.id,
            started_at=datetime.now(timezone.utc),
        )
        
        db_session.add(session)
        await db_session.commit()
        await db_session.refresh(session)
        
        assert session.id is not None
        assert session.hint_requests == 0
        assert session.code_runs == 0
        assert session.completed == False
    
    @pytest.mark.asyncio
    async def test_session_metrics_increment(self, db_session):
        """Test incrementing session metrics."""
        from app.models.user import User
        from app.models.session import LearningSession
        
        user = User(
            username="metricsuser2",
            hashed_password="hashed",
            birth_year=2010,
            grade_level=7,
        )
        db_session.add(user)
        await db_session.commit()
        
        session = LearningSession(user_id=user.id)
        db_session.add(session)
        await db_session.commit()
        
        # Increment metrics
        session.hint_requests += 1
        session.code_runs += 3
        session.errors_encountered += 2
        session.frustration_events += 1
        
        await db_session.commit()
        await db_session.refresh(session)
        
        assert session.hint_requests == 1
        assert session.code_runs == 3
        assert session.errors_encountered == 2
        assert session.frustration_events == 1


class TestExerciseProgressModel:
    """Tests for ExerciseProgress model."""
    
    @pytest.mark.asyncio
    async def test_progress_creation(self, db_session):
        """Test creating exercise progress."""
        from app.models.user import User
        from app.models.session import Exercise, ExerciseProgress
        
        # Create user and exercise
        user = User(
            username="progressuser",
            hashed_password="hashed",
            birth_year=2010,
            grade_level=7,
        )
        exercise = Exercise(
            title="Progress Exercise",
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
        
        # Create progress
        progress = ExerciseProgress(
            user_id=user.id,
            exercise_id=exercise.id,
            current_step=1,
        )
        
        db_session.add(progress)
        await db_session.commit()
        await db_session.refresh(progress)
        
        assert progress.id is not None
        assert progress.completed == False
        assert progress.points_earned == 0
        assert progress.hints_used == 0

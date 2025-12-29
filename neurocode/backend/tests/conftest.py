"""
Pytest configuration and fixtures for PyPal backend tests.
"""
import pytest
import asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.main import app
from app.database import Base, get_db
from app.config import get_settings

# Test database
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test_pypal.db"


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_engine():
    """Create test database engine."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


@pytest.fixture
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session."""
    async_session_maker = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    async with async_session_maker() as session:
        yield session
        await session.rollback()


@pytest.fixture
async def client(db_session) -> AsyncGenerator[AsyncClient, None]:
    """Create test client with database override."""
    
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()


@pytest.fixture
def settings():
    """Get application settings."""
    return get_settings()


@pytest.fixture
def sample_user_data():
    """Sample user registration data."""
    return {
        "username": "testuser",
        "password": "securepassword123",
        "birth_year": 2010,  # Under 13, needs consent
        "grade_level": 7,
        "parent_email": "parent@example.com",
    }


@pytest.fixture
def sample_user_data_13plus():
    """Sample user registration data for 13+ (no consent needed)."""
    return {
        "username": "teenuser",
        "password": "securepassword123",
        "birth_year": 2009,  # 13+
        "grade_level": 8,
    }


@pytest.fixture
def sample_exercise_data():
    """Sample exercise creation data."""
    return {
        "title": "Test Exercise",
        "description": "A test exercise for unit testing",
        "difficulty": 1,
        "starter_code": "# Write your code here\n",
        "solution_code": 'print("Hello!")',
        "concept": "print",
        "grade_level": 6,
        "estimated_minutes": 5,
        "step_count": 2,
    }

"""
Async SQLAlchemy database configuration using SQLite for development.
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.config import get_settings

settings = get_settings()

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
)

# Session factory
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Base class for all models."""
    pass


async def get_db():
    """Dependency for getting database sessions."""
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    """Initialize database tables and apply lightweight column migrations."""
    print("[DB] Initializing database...")
    # Import models to register them with Base.metadata
    from app.models import (
        User, ParentalConsent, Exercise,
        LearningSession, TutorInteraction, ExerciseProgress
    )
    print(f"[DB] Loaded {len(Base.metadata.tables)} tables: {list(Base.metadata.tables.keys())}")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # Lightweight SQLite migrations for columns added after initial release.
        await _ensure_user_columns(conn)
    print("[DB] Database initialized successfully!")


async def _ensure_user_columns(conn):
    """Add columns introduced after the initial schema, idempotently (SQLite)."""
    from sqlalchemy import text

    def _apply(sync_conn):
        cols = {row[1] for row in sync_conn.exec_driver_sql("PRAGMA table_info(users)").fetchall()}
        migrations = [
            ("role", "ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'student'"),
            ("display_name", "ALTER TABLE users ADD COLUMN display_name VARCHAR(100)"),
            ("school", "ALTER TABLE users ADD COLUMN school VARCHAR(200)"),
        ]
        for col, ddl in migrations:
            if col not in cols:
                sync_conn.exec_driver_sql(ddl)
                print(f"[DB] Migrated users: added column {col}")

    await conn.run_sync(_apply)
    # Silence unused import noise
    _ = text

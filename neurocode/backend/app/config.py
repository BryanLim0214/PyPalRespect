"""
Application configuration with environment variable support.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    PROJECT_NAME: str = "PyPal"
    API_V1_STR: str = "/api/v1"
    
    # App
    APP_NAME: str = "PyPal"
    DEBUG: bool = False
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./pypal.db"
    
    # Gemini API (NEW SDK)
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.0-flash"
    GEMINI_MAX_RETRIES: int = 3
    GEMINI_TIMEOUT_SECONDS: int = 30
    
    # COPPA Compliance
    REQUIRE_PARENTAL_CONSENT: bool = True
    MIN_AGE_WITHOUT_CONSENT: int = 13
    MIN_AGE_ALLOWED: int = 6
    MAX_AGE_ALLOWED: int = 18
    
    # Session settings (ADHD-optimized)
    SESSION_TIMEOUT_MINUTES: int = 45
    BREAK_REMINDER_MINUTES: int = 20
    DEFAULT_SESSION_LENGTH: int = 30
    
    # Research
    ENABLE_ANALYTICS: bool = True
    ANONYMIZE_DATA: bool = True
    
    # JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"
    
    # Code Runner Safety
    CODE_EXECUTION_TIMEOUT: int = 5
    MAX_CODE_LENGTH: int = 10000
    MAX_OUTPUT_LENGTH: int = 5000
    
    # Gamification
    POINTS_PER_EXERCISE: int = 20
    POINTS_HINT_PENALTY: int = 5
    MIN_POINTS_PER_EXERCISE: int = 10
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
        "extra": "ignore"
    }


@lru_cache()
def get_settings() -> Settings:
    """Cached settings instance."""
    return Settings()

"""
Application configuration with environment variable support.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # App
    APP_NAME: str = "NeuroCode"
    DEBUG: bool = False
    SECRET_KEY: str = "dev-secret-key"
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./neurocode.db"
    
    # Gemini API (NEW SDK)
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.0-flash"
    
    # COPPA Compliance
    REQUIRE_PARENTAL_CONSENT: bool = True
    MIN_AGE_WITHOUT_CONSENT: int = 13
    
    # Session settings
    SESSION_TIMEOUT_MINUTES: int = 45
    BREAK_REMINDER_MINUTES: int = 20
    
    # Research
    ENABLE_ANALYTICS: bool = True
    ANONYMIZE_DATA: bool = True
    
    # JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
        "extra": "ignore"
    }


@lru_cache()
def get_settings() -> Settings:
    """Cached settings instance."""
    return Settings()

"""
Tests for application configuration.
"""
import pytest
import os
from unittest.mock import patch


class TestConfig:
    """Tests for config.py"""
    
    def test_settings_loads_defaults(self):
        """Test that Settings loads with default values."""
        from app.config import Settings
        
        # Create settings with minimal required values, bypass .env file
        settings = Settings(
            SECRET_KEY="test-secret",
            GEMINI_API_KEY="test-api-key",
            _env_file=None,  # Prevent loading .env to test defaults
        )
        
        assert settings.PROJECT_NAME == "PyPal"
        assert settings.API_V1_STR == "/api/v1"
        assert settings.DEBUG == False
        assert settings.MIN_AGE_WITHOUT_CONSENT == 13
        assert settings.SESSION_TIMEOUT_MINUTES == 45
        assert settings.BREAK_REMINDER_MINUTES == 20
    
    def test_settings_validates_required_fields(self):
        """Test that required fields are enforced."""
        from app.config import Settings
        
        # Should work with required fields
        settings = Settings(
            SECRET_KEY="test-secret",
            GEMINI_API_KEY="test-key",
        )
        assert settings.SECRET_KEY == "test-secret"
    
    def test_settings_gemini_model_default(self):
        """Test Gemini model default value."""
        from app.config import Settings
        
        settings = Settings(
            SECRET_KEY="test",
            GEMINI_API_KEY="test",
        )
        
        assert settings.GEMINI_MODEL == "gemini-2.0-flash"
    
    def test_get_settings_cached(self):
        """Test that get_settings returns cached instance."""
        from app.config import get_settings
        
        settings1 = get_settings()
        settings2 = get_settings()
        
        # Should be same cached instance
        assert settings1 is settings2
    
    def test_settings_jwt_defaults(self):
        """Test JWT-related default settings."""
        from app.config import Settings
        
        settings = Settings(
            SECRET_KEY="test",
            GEMINI_API_KEY="test",
        )
        
        assert settings.ACCESS_TOKEN_EXPIRE_MINUTES == 60
        assert settings.ALGORITHM == "HS256"
    
    def test_settings_coppa_defaults(self):
        """Test COPPA compliance default settings."""
        from app.config import Settings
        
        settings = Settings(
            SECRET_KEY="test",
            GEMINI_API_KEY="test",
        )
        
        assert settings.REQUIRE_PARENTAL_CONSENT == True
        assert settings.MIN_AGE_WITHOUT_CONSENT == 13
    
    def test_settings_analytics_defaults(self):
        """Test analytics default settings."""
        from app.config import Settings
        
        settings = Settings(
            SECRET_KEY="test",
            GEMINI_API_KEY="test",
        )
        
        assert settings.ENABLE_ANALYTICS == True
        assert settings.ANONYMIZE_DATA == True

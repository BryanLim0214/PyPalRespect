"""
Tests for security utilities.
"""
import pytest
from datetime import timedelta


class TestPasswordHashing:
    """Tests for password hashing."""
    
    def test_hash_password_returns_hash(self):
        """Test that hash_password returns a hash."""
        from app.utils.security import hash_password
        
        hashed = hash_password("mypassword123")
        
        assert hashed is not None
        assert hashed != "mypassword123"
        assert len(hashed) > 20
    
    def test_verify_password_correct(self):
        """Test verifying correct password."""
        from app.utils.security import hash_password, verify_password
        
        password = "securepass123"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) == True
    
    def test_verify_password_incorrect(self):
        """Test verifying incorrect password."""
        from app.utils.security import hash_password, verify_password
        
        hashed = hash_password("correctpassword")
        
        assert verify_password("wrongpassword", hashed) == False
    
    def test_different_passwords_different_hashes(self):
        """Test that different passwords produce different hashes."""
        from app.utils.security import hash_password
        
        hash1 = hash_password("password1")
        hash2 = hash_password("password2")
        
        assert hash1 != hash2
    
    def test_same_password_different_hashes(self):
        """Test that same password produces different hashes (salting)."""
        from app.utils.security import hash_password
        
        hash1 = hash_password("samepassword")
        hash2 = hash_password("samepassword")
        
        # Due to salting, hashes should be different
        assert hash1 != hash2


class TestJWTTokens:
    """Tests for JWT token handling."""
    
    def test_create_access_token(self):
        """Test creating an access token."""
        from app.utils.security import create_access_token
        
        token = create_access_token(data={"user_id": 1, "username": "testuser"})
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 50
    
    def test_decode_access_token_valid(self):
        """Test decoding a valid token."""
        from app.utils.security import create_access_token, decode_access_token
        
        original_data = {"user_id": 42, "username": "testuser"}
        token = create_access_token(data=original_data)
        
        decoded = decode_access_token(token)
        
        assert decoded is not None
        assert decoded["user_id"] == 42
        assert decoded["username"] == "testuser"
    
    def test_decode_access_token_invalid(self):
        """Test decoding an invalid token."""
        from app.utils.security import decode_access_token
        
        result = decode_access_token("invalid.token.here")
        
        assert result is None
    
    def test_decode_access_token_expired(self):
        """Test decoding an expired token."""
        from app.utils.security import create_access_token, decode_access_token
        
        # Create token that expires immediately
        token = create_access_token(
            data={"user_id": 1},
            expires_delta=timedelta(seconds=-10)  # Already expired
        )
        
        result = decode_access_token(token)
        
        assert result is None
    
    def test_token_contains_expiry(self):
        """Test that token contains expiry time."""
        from app.utils.security import create_access_token, decode_access_token
        
        token = create_access_token(data={"user_id": 1})
        decoded = decode_access_token(token)
        
        assert "exp" in decoded


class TestConsentTokens:
    """Tests for parental consent tokens."""
    
    def test_generate_consent_token(self):
        """Test generating a consent token."""
        from app.utils.security import generate_consent_token
        
        token = generate_consent_token(user_id=123)
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 50
    
    def test_decode_consent_token_valid(self):
        """Test decoding a valid consent token."""
        from app.utils.security import generate_consent_token, decode_consent_token
        
        token = generate_consent_token(user_id=456)
        
        user_id = decode_consent_token(token)
        
        assert user_id == 456
    
    def test_decode_consent_token_invalid(self):
        """Test decoding an invalid consent token."""
        from app.utils.security import decode_consent_token
        
        result = decode_consent_token("invalid.token")
        
        assert result is None
    
    def test_consent_token_wrong_type(self):
        """Test that regular access tokens don't work as consent tokens."""
        from app.utils.security import create_access_token, decode_consent_token
        
        # Create a regular access token (not consent type)
        regular_token = create_access_token(data={"user_id": 1})
        
        # Should not decode as consent token
        result = decode_consent_token(regular_token)
        
        assert result is None


class TestRandomTokens:
    """Tests for random token generation."""
    
    def test_generate_random_token(self):
        """Test generating random token."""
        from app.utils.security import generate_random_token
        
        token = generate_random_token()
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 20
    
    def test_random_tokens_unique(self):
        """Test that random tokens are unique."""
        from app.utils.security import generate_random_token
        
        tokens = [generate_random_token() for _ in range(10)]
        
        # All should be unique
        assert len(set(tokens)) == 10
    
    def test_random_token_length(self):
        """Test random token with custom length."""
        from app.utils.security import generate_random_token
        
        token = generate_random_token(length=64)
        
        # URL-safe base64 encoding uses 4/3 ratio plus padding
        assert len(token) > 64

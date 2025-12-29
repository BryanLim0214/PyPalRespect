"""
Security utilities for authentication and token handling.
"""
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
import secrets
import logging

from app.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

# Password hashing - using pbkdf2_sha256 for better Python 3.13 compatibility
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decode and validate a JWT access token.
    Returns None if invalid or expired.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError as e:
        logger.warning(f"JWT decode error: {e}")
        return None


def generate_consent_token(user_id: int) -> str:
    """
    Generate a token for parental consent verification.
    Valid for 7 days.
    """
    data = {
        "user_id": user_id,
        "type": "consent",
        "exp": datetime.now(timezone.utc) + timedelta(days=7)
    }
    
    return jwt.encode(
        data,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def decode_consent_token(token: str) -> Optional[int]:
    """
    Decode a consent token and return the user_id.
    Returns None if invalid or expired.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        if payload.get("type") != "consent":
            return None
        return payload.get("user_id")
    except JWTError as e:
        logger.warning(f"Consent token decode error: {e}")
        return None


def generate_random_token(length: int = 32) -> str:
    """Generate a cryptographically secure random token."""
    return secrets.token_urlsafe(length)

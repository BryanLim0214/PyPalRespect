"""
Tests for authentication routes including COPPA compliance.
"""
import pytest
from datetime import date


class TestRegistration:
    """Tests for user registration."""
    
    @pytest.mark.asyncio
    async def test_register_13_plus_user(self, client, db_session):
        """Test registration for user 13 or older (no consent needed)."""
        current_year = date.today().year
        birth_year = current_year - 14  # 14 years old
        
        response = await client.post("/api/auth/register", json={
            "username": "teenuser1",
            "password": "securepass123",
            "birth_year": birth_year,
            "grade_level": 8,
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "registered"
        assert "access_token" in data
    
    @pytest.mark.asyncio
    async def test_register_under_13_requires_consent(self, client, db_session):
        """Test registration for user under 13 requires parent consent."""
        current_year = date.today().year
        birth_year = current_year - 11  # 11 years old
        
        response = await client.post("/api/auth/register", json={
            "username": "younguser1",
            "password": "securepass123",
            "birth_year": birth_year,
            "grade_level": 6,
            "parent_email": "parent@example.com",
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "consent_required"
        assert "consent_token" in data
    
    @pytest.mark.asyncio
    async def test_register_under_13_without_parent_email(self, client, db_session):
        """Test registration fails for under 13 without parent email."""
        current_year = date.today().year
        birth_year = current_year - 10  # 10 years old
        
        response = await client.post("/api/auth/register", json={
            "username": "younguser2",
            "password": "securepass123",
            "birth_year": birth_year,
            "grade_level": 6,
            # No parent_email
        })
        
        assert response.status_code == 400
        assert "parent email" in response.json()["detail"].lower()
    
    @pytest.mark.asyncio
    async def test_register_duplicate_username(self, client, db_session):
        """Test registration fails for duplicate username."""
        current_year = date.today().year
        birth_year = current_year - 14
        
        # First registration
        await client.post("/api/auth/register", json={
            "username": "duplicateuser",
            "password": "securepass123",
            "birth_year": birth_year,
            "grade_level": 7,
        })
        
        # Second registration with same username
        response = await client.post("/api/auth/register", json={
            "username": "duplicateuser",
            "password": "differentpass",
            "birth_year": birth_year,
            "grade_level": 8,
        })
        
        assert response.status_code == 400
        assert "taken" in response.json()["detail"].lower()
    
    @pytest.mark.asyncio
    async def test_register_invalid_age(self, client, db_session):
        """Test registration fails for invalid age."""
        current_year = date.today().year
        
        # Too young (5 years old)
        response = await client.post("/api/auth/register", json={
            "username": "tooyoung",
            "password": "securepass123",
            "birth_year": current_year - 5,
            "grade_level": 6,
        })
        
        assert response.status_code == 400


class TestConsentVerification:
    """Tests for parental consent verification."""
    
    @pytest.mark.asyncio
    async def test_verify_consent_granted(self, client, db_session):
        """Test consent verification when parent approves."""
        from app.utils.security import generate_consent_token
        from app.models.user import User
        
        # Create a user needing consent
        user = User(
            username="consentchild",
            hashed_password="hashed",
            birth_year=2014,
            grade_level=6,
            parent_email="parent@test.com",
            has_parental_consent=False,
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        
        token = generate_consent_token(user.id)
        
        response = await client.post("/api/auth/consent/verify", json={
            "token": token,
            "consent_given": True,
            "research_consent": True,
            "data_sharing_consent": False,
        })
        
        assert response.status_code == 200
        assert response.json()["status"] == "consent_recorded"
    
    @pytest.mark.asyncio
    async def test_verify_consent_denied(self, client, db_session):
        """Test consent verification when parent denies."""
        from app.utils.security import generate_consent_token
        from app.models.user import User
        
        user = User(
            username="deletechild",
            hashed_password="hashed",
            birth_year=2014,
            grade_level=6,
            parent_email="parent@test.com",
            has_parental_consent=False,
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        
        token = generate_consent_token(user.id)
        
        response = await client.post("/api/auth/consent/verify", json={
            "token": token,
            "consent_given": False,
        })
        
        assert response.status_code == 200
        assert response.json()["status"] == "consent_denied"
    
    @pytest.mark.asyncio
    async def test_verify_consent_invalid_token(self, client, db_session):
        """Test consent verification with invalid token."""
        response = await client.post("/api/auth/consent/verify", json={
            "token": "invalid_token_here",
            "consent_given": True,
        })
        
        assert response.status_code == 400


class TestLogin:
    """Tests for user login."""
    
    @pytest.mark.asyncio
    async def test_login_success(self, client, db_session):
        """Test successful login."""
        current_year = date.today().year
        
        # Register user first
        await client.post("/api/auth/register", json={
            "username": "loginuser",
            "password": "testpass123",
            "birth_year": current_year - 14,
            "grade_level": 8,
        })
        
        # Login
        response = await client.post(
            "/api/auth/login",
            data={"username": "loginuser", "password": "testpass123"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    @pytest.mark.asyncio
    async def test_login_wrong_password(self, client, db_session):
        """Test login with wrong password."""
        current_year = date.today().year
        
        await client.post("/api/auth/register", json={
            "username": "wrongpassuser",
            "password": "correctpass",
            "birth_year": current_year - 14,
            "grade_level": 8,
        })
        
        response = await client.post(
            "/api/auth/login",
            data={"username": "wrongpassuser", "password": "wrongpass"}
        )
        
        assert response.status_code == 401
    
    @pytest.mark.asyncio
    async def test_login_without_consent(self, client, db_session):
        """Test login fails for user without parental consent."""
        from app.models.user import User
        from app.utils.security import hash_password
        
        user = User(
            username="noconsentuser",
            hashed_password=hash_password("testpass"),
            birth_year=2014,
            grade_level=6,
            has_parental_consent=False,
        )
        db_session.add(user)
        await db_session.commit()
        
        response = await client.post(
            "/api/auth/login",
            data={"username": "noconsentuser", "password": "testpass"}
        )
        
        assert response.status_code == 403
        assert "consent" in response.json()["detail"].lower()


class TestGetMe:
    """Tests for getting current user profile."""
    
    @pytest.mark.asyncio
    async def test_get_me_authenticated(self, client, db_session):
        """Test getting profile when authenticated."""
        current_year = date.today().year
        
        # Register and login
        await client.post("/api/auth/register", json={
            "username": "meuser",
            "password": "testpass123",
            "birth_year": current_year - 14,
            "grade_level": 8,
        })
        
        login_response = await client.post(
            "/api/auth/login",
            data={"username": "meuser", "password": "testpass123"}
        )
        token = login_response.json()["access_token"]
        
        # Get profile
        response = await client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "meuser"
        assert data["grade_level"] == 8
    
    @pytest.mark.asyncio
    async def test_get_me_unauthenticated(self, client, db_session):
        """Test getting profile without authentication."""
        response = await client.get("/api/auth/me")
        
        assert response.status_code == 401

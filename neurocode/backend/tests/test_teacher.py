"""
Tests for teacher registration, role-based access, and teacher endpoints.
"""
import pytest
from datetime import date


async def _register_teacher(client, username="msrivera"):
    response = await client.post("/api/auth/register", json={
        "username": username,
        "password": "securepass123",
        "birth_year": 1990,
        "grade_level": 0,
        "role": "teacher",
        "display_name": "Ms. Rivera",
        "school": "Washington Middle",
    })
    return response


async def _register_student(client, username="student1", age=14):
    year = date.today().year
    response = await client.post("/api/auth/register", json={
        "username": username,
        "password": "securepass123",
        "birth_year": year - age,
        "grade_level": 8,
    })
    return response


class TestTeacherRegistration:
    @pytest.mark.asyncio
    async def test_teacher_register_succeeds(self, client):
        response = await _register_teacher(client, "teacher_a")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "registered"
        assert data["user"]["role"] == "teacher"
        assert data["user"]["display_name"] == "Ms. Rivera"

    @pytest.mark.asyncio
    async def test_teacher_can_login(self, client):
        await _register_teacher(client, "teacher_b")
        response = await client.post(
            "/api/auth/login",
            data={"username": "teacher_b", "password": "securepass123"},
        )
        assert response.status_code == 200
        assert "access_token" in response.json()


class TestTeacherAccessControl:
    @pytest.mark.asyncio
    async def test_student_cannot_access_teacher_endpoint(self, client):
        await _register_student(client, "stu_a", 14)
        login = await client.post(
            "/api/auth/login",
            data={"username": "stu_a", "password": "securepass123"},
        )
        token = login.json()["access_token"]

        response = await client.get(
            "/api/teacher/overview",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_unauthenticated_cannot_access_teacher_endpoint(self, client):
        response = await client.get("/api/teacher/overview")
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_teacher_can_access_overview(self, client):
        await _register_teacher(client, "teacher_c")
        login = await client.post(
            "/api/auth/login",
            data={"username": "teacher_c", "password": "securepass123"},
        )
        token = login.json()["access_token"]

        response = await client.get(
            "/api/teacher/overview",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "total_students" in data
        assert "total_exercises" in data


class TestTeacherStudentListing:
    @pytest.mark.asyncio
    async def test_teacher_sees_students(self, client):
        await _register_student(client, "stu_listed", 14)
        await _register_teacher(client, "teacher_d")
        login = await client.post(
            "/api/auth/login",
            data={"username": "teacher_d", "password": "securepass123"},
        )
        token = login.json()["access_token"]

        response = await client.get(
            "/api/teacher/students",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        usernames = [row["username"] for row in response.json()]
        assert "stu_listed" in usernames

    @pytest.mark.asyncio
    async def test_student_detail_returns_summary_fields(self, client, db_session):
        """Student detail response includes top-level completion/attempt counts."""
        from app.models.user import User
        from app.utils.security import hash_password

        student = User(
            username="stu_det",
            hashed_password=hash_password("x"),
            birth_year=2010,
            grade_level=7,
            has_parental_consent=True,
            role="student",
        )
        db_session.add(student)
        await db_session.commit()
        await db_session.refresh(student)

        await _register_teacher(client, "teacher_f")
        login = await client.post(
            "/api/auth/login",
            data={"username": "teacher_f", "password": "securepass123"},
        )
        token = login.json()["access_token"]

        response = await client.get(
            f"/api/teacher/students/{student.id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        for key in ("exercises_attempted", "exercises_completed", "hints_used"):
            assert key in data

    @pytest.mark.asyncio
    async def test_teacher_student_detail_404_on_wrong_role(self, client):
        await _register_teacher(client, "teacher_e")
        login = await client.post(
            "/api/auth/login",
            data={"username": "teacher_e", "password": "securepass123"},
        )
        token = login.json()["access_token"]

        # Teachers shouldn't be returned by /teacher/students; asking for
        # a non-existent student id should 404.
        response = await client.get(
            "/api/teacher/students/9999",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404

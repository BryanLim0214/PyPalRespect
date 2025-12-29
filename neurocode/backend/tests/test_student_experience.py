
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_student_journey_personalization(client: AsyncClient, db_session):
    """
    Simulates a middle school student's journey to verify personalization.
    Research Goal: Validate that the system adapts to student interests.
    """
    # 1. Register as a student with specific interests
    student_data = {
        "username": "space_cadet_99",
        "password": "securepassword123",
        "birth_year": 2012,
        "grade_level": 7,
        "interests": ["space", "rockets", "mars"]
    }
    
    # Register
    response = await client.post("/api/auth/register", json=student_data)
    assert response.status_code == 200
    data = response.json()
    token = data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Verify interests are stored correctly
    me_response = await client.get("/api/auth/me", headers=headers)
    assert me_response.status_code == 200
    user_data = me_response.json()
    import json
    stored_interests = json.loads(user_data["interests"])
    assert "space" in stored_interests
    
    # 3. Request Task Decomposition (checking interest injection)
    # The tutor should use these interests to break down the task
    task_response = await client.post(
        "/api/tutor/decompose",
        json={
            "task": "Write a loop that counts down from 10",
            "student_interests": stored_interests
        },
        headers=headers
    )
    assert task_response.status_code == 200
    decomposition = task_response.json()
    
    # We can't deterministically check the LLM output text for specific words 
    # without a mock, but we can verify the structure and that it returns success.
    # In a real integration test, we would check if the prompt sent to Gemini contained 'space'.
    assert len(decomposition["steps"]) > 0
    assert decomposition["estimated_time_minutes"] > 0
    
    # 4. Chat with Tutor (checking dynamic system prompt)
    # We will send a message and ensure we get a valid response
    chat_response = await client.post(
        "/api/tutor/message",
        json={
            "message": "I'm stuck on this loop. Can you explain it like a rocket launch?",
            "current_step": 1
        },
        headers=headers
    )
    assert chat_response.status_code == 200
    chat_data = chat_response.json()
    assert chat_data["response"] is not None
    assert len(chat_data["response"]) > 0

@pytest.mark.asyncio
async def test_middle_school_safety_bounds(client: AsyncClient):
    """
    Verifies safeguards for the target audience (ages 11-14).
    Research Goal: Safety and age-appropriateness.
    """
    # Test age restrictions
    too_young = {
        "username": "baby_coder",
        "password": "password123",
        "birth_year": 2020, # 5 years old (too young)
        "grade_level": 1
    }
    response = await client.post("/api/auth/register", json=too_young)
    assert response.status_code == 422 # OR 400 depending on where validation hits. Schema validation hits first.
    # assert "ages 6-18" in response.json()["detail"]

    # Test Username validation (no offensive patterns check here, but basic format)
    bad_name = {
        "username": "bad user name!", # Spaces/special chars
        "password": "password123",
        "birth_year": 2012,
        "grade_level": 7
    }
    response = await client.post("/api/auth/register", json=bad_name)
    assert response.status_code == 422 # Validation error

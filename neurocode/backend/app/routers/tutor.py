"""
Tutor API routes for LLM-powered tutoring.
"""
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.models.session import LearningSession, TutorInteraction
from app.schemas.tutor import (
    TutorMessage,
    TutorResponse,
    HintRequest,
    HintResponse,
    TaskDecompositionRequest,
    TaskDecompositionResponse,
)
from app.services.gemini_service import gemini_service
from app.services.task_decomposer import task_decomposer
from app.services.hint_generator import hint_generator
from app.services.analytics import AnalyticsService
from app.prompts.system_prompts import get_tutor_system_prompt
from app.routers.auth import get_current_user

router = APIRouter()


@router.get("/test")
async def test_gemini():
    """Test Gemini API connectivity."""
    try:
        success = await gemini_service.test_connection()
        return {
            "status": "connected" if success else "failed",
            "model": gemini_service.model
        }
    except Exception as e:
        return {
            "status": "error",
            "detail": str(e)
        }


@router.post("/message", response_model=TutorResponse)
async def send_message(
    message: TutorMessage,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Send a message to the tutor and get a response.
    """
    # Get or create session
    session = None
    if message.session_id:
        session = await db.get(LearningSession, message.session_id)
    
    if not session:
        session = LearningSession(
            user_id=current_user.id,
            started_at=datetime.now(timezone.utc)
        )
        db.add(session)
        await db.commit()
        await db.refresh(session)
    
    # Get conversation history from session
    conversation_history = await _get_conversation_history(db, session.id)
    
    # Record student message
    student_interaction = TutorInteraction(
        session_id=session.id,
        role="student",
        content=message.message,
        current_step=message.current_step,
        code_snapshot=message.current_code,
        timestamp=datetime.now(timezone.utc),
    )
    db.add(student_interaction)
    
    # Detect frustration
    frustration_keywords = ["stuck", "don't get", "confused", "help", "frustrated", "hard"]
    is_frustrated = any(kw in message.message.lower() for kw in frustration_keywords)
    
    if is_frustrated:
        analytics = AnalyticsService(db)
        await analytics.log_session_event(session.id, "frustration_expressed")
    
    # Get user interests
    import json
    user_interests = []
    if current_user.interests:
        try:
            user_interests = json.loads(current_user.interests)
        except:
            pass
            
    # Generate response
    try:
        system_prompt = get_tutor_system_prompt(user_interests)
        response_text = await gemini_service.generate_response(
            user_message=message.message,
            system_prompt=system_prompt,
            conversation_history=conversation_history,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tutor error: {str(e)}")
    
    # Record tutor response
    tutor_interaction = TutorInteraction(
        session_id=session.id,
        role="tutor",
        content=response_text,
        current_step=message.current_step,
        timestamp=datetime.now(timezone.utc),
    )
    db.add(tutor_interaction)
    await db.commit()
    
    # Check for celebrations
    celebration_keywords = ["did it", "got it", "works", "done", "finished"]
    is_celebration = any(kw in message.message.lower() for kw in celebration_keywords)
    
    return TutorResponse(
        response=response_text,
        is_step=message.current_step is not None,
        step_number=message.current_step,
        celebration=is_celebration,
        points_earned=10 if is_celebration else 0,
    )


@router.post("/message/stream")
async def send_message_stream(
    message: TutorMessage,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Stream a response from the tutor.
    Useful for keeping ADHD learners engaged with real-time text.
    """
    conversation_history = []
    if message.session_id:
        conversation_history = await _get_conversation_history(db, message.session_id)
    
    # Get user interests
    import json
    user_interests = []
    if current_user.interests:
        try:
            user_interests = json.loads(current_user.interests)
        except:
            pass

    async def generate():
        system_prompt = get_tutor_system_prompt(user_interests)
        async for chunk in gemini_service.generate_response_stream(
            user_message=message.message,
            system_prompt=system_prompt,
            conversation_history=conversation_history,
        ):
            yield chunk
    
    return StreamingResponse(generate(), media_type="text/plain")


@router.post("/hint", response_model=HintResponse)
async def get_hint(
    request: HintRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get a hint for the current code.
    Hints escalate from gentle nudges (level 1) to full solutions (level 4).
    """
    hint_response = await hint_generator.generate_hint(
        code=request.code,
        error_message=request.error_message,
        hint_level=request.hint_level,
    )
    
    return hint_response


@router.post("/decompose", response_model=TaskDecompositionResponse)
async def decompose_task(
    request: TaskDecompositionRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Break a coding task into ADHD-friendly micro-steps.
    """
    result = await task_decomposer.decompose_task(
        task=request.task,
        student_interests=request.student_interests,
    )
    
    return result


async def _get_conversation_history(
    db: AsyncSession, 
    session_id: int,
    limit: int = 10
) -> List[dict]:
    """Get recent conversation history for context."""
    from sqlalchemy import select
    
    result = await db.execute(
        select(TutorInteraction)
        .where(TutorInteraction.session_id == session_id)
        .order_by(TutorInteraction.timestamp.desc())
        .limit(limit)
    )
    
    interactions = result.scalars().all()
    
    # Convert to format expected by Gemini
    history = []
    for interaction in reversed(interactions):
        role = "user" if interaction.role == "student" else "model"
        history.append({
            "role": role,
            "content": interaction.content
        })
    
    return history

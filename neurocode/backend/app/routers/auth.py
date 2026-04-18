"""
Authentication routes with COPPA-compliant consent flow.
"""
from datetime import datetime, date, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.user import User, ParentalConsent
from app.schemas.user import (
    RegisterRequest, 
    ConsentRequest, 
    UserResponse, 
    Token,
    UserPreferencesUpdate,
)
from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
    generate_consent_token,
    decode_consent_token,
)
from app.config import get_settings

router = APIRouter()
settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Get current user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    user_id = payload.get("user_id")
    if user_id is None:
        raise credentials_exception

    user = await db.get(User, user_id)
    if user is None:
        raise credentials_exception

    return user


async def require_teacher(current_user: User = Depends(get_current_user)) -> User:
    """Only allow users with the teacher role."""
    if current_user.role != "teacher":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Teacher access required",
        )
    return current_user


@router.post("/register")
async def register_student(
    request: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Register a new student or teacher.
    Students under 13 trigger the parental consent flow (COPPA compliance).
    Teachers skip age/grade validation and are activated immediately.
    """
    # Check if username exists
    result = await db.execute(
        select(User).where(User.username == request.username.lower())
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Username already taken"
        )

    import json

    # Teacher registration path
    if request.role == "teacher":
        teacher = User(
            username=request.username.lower(),
            hashed_password=hash_password(request.password),
            role="teacher",
            display_name=request.display_name or request.username,
            school=request.school,
            birth_year=request.birth_year or 1990,
            grade_level=0,
            has_parental_consent=True,
            consent_date=datetime.now(timezone.utc),
        )
        db.add(teacher)
        await db.commit()
        await db.refresh(teacher)

        access_token = create_access_token(
            data={"user_id": teacher.id, "username": teacher.username, "role": "teacher"}
        )
        return {
            "status": "registered",
            "access_token": access_token,
            "token_type": "bearer",
            "user": UserResponse.model_validate(teacher),
        }

    # Calculate age and validate against configured bounds (student path)
    current_year = date.today().year
    age = current_year - request.birth_year

    if age < settings.MIN_AGE_ALLOWED or age > settings.MAX_AGE_ALLOWED:
        raise HTTPException(
            status_code=400,
            detail=f"This platform is for students ages {settings.MIN_AGE_ALLOWED}-{settings.MAX_AGE_ALLOWED}"
        )

    if request.grade_level < 6 or request.grade_level > 8:
        raise HTTPException(
            status_code=400,
            detail="Grade level must be 6, 7, or 8",
        )

    # Create user
    user = User(
        username=request.username.lower(),
        hashed_password=hash_password(request.password),
        role="student",
        birth_year=request.birth_year,
        grade_level=request.grade_level,
        has_parental_consent=False,
        interests=json.dumps(request.interests) if request.interests else None,
    )

    if age < settings.MIN_AGE_WITHOUT_CONSENT:
        # COPPA: Require parental consent
        if not request.parent_email:
            raise HTTPException(
                status_code=400,
                detail="Parent email required for students under 13"
            )
        
        user.parent_email = request.parent_email
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        # Generate consent token
        consent_token = generate_consent_token(user.id)
        
        # In production, send email here
        # await send_parental_consent_email(...)
        
        return {
            "status": "consent_required",
            "message": "We sent an email to your parent/guardian. They need to give permission before you can start coding!",
            "consent_token": consent_token,  # For testing
        }
    else:
        # 13+ can consent for themselves
        user.has_parental_consent = True
        user.consent_date = datetime.now(timezone.utc)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        # Create access token
        access_token = create_access_token(
            data={"user_id": user.id, "username": user.username, "role": user.role}
        )

        return {
            "status": "registered",
            "access_token": access_token,
            "token_type": "bearer",
            "user": UserResponse.model_validate(user)
        }


@router.post("/consent/verify")
async def verify_parental_consent(
    request: ConsentRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Verify parental consent from email link (COPPA compliance).
    """
    # Decode token
    user_id = decode_consent_token(request.token)
    if not user_id:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired consent link"
        )
    
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.has_parental_consent:
        return {"status": "already_consented", "message": "Consent already recorded"}
    
    if request.consent_given:
        # Record consent
        consent = ParentalConsent(
            user_id=user.id,
            parent_email=user.parent_email,
            consent_given=True,
            consent_timestamp=datetime.now(timezone.utc),
            consent_method="email_link",
            research_consent=request.research_consent,
            data_sharing_consent=request.data_sharing_consent,
        )
        user.has_parental_consent = True
        user.consent_date = datetime.now(timezone.utc)
        
        db.add(consent)
        await db.commit()
        
        return {
            "status": "consent_recorded",
            "message": "Thank you! Your child can now start coding."
        }
    else:
        # Parent denied - delete the pending account
        await db.delete(user)
        await db.commit()
        
        return {
            "status": "consent_denied",
            "message": "Account request cancelled."
        }


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """Login with username and password."""
    result = await db.execute(
        select(User).where(User.username == form_data.username.lower())
    )
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.has_parental_consent:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Awaiting parental consent"
        )
    
    # Update last active
    user.last_active = datetime.now(timezone.utc)
    await db.commit()
    
    access_token = create_access_token(
        data={"user_id": user.id, "username": user.username, "role": user.role}
    )

    return Token(access_token=access_token)


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current user profile."""
    return UserResponse.model_validate(current_user)


@router.patch("/me")
async def update_preferences(
    updates: UserPreferencesUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update user preferences."""
    if updates.adhd_profile is not None:
        current_user.adhd_profile = updates.adhd_profile
    if updates.interests is not None:
        import json
        current_user.interests = json.dumps(updates.interests)
    if updates.preferred_break_interval is not None:
        current_user.preferred_break_interval = updates.preferred_break_interval
    if updates.preferred_session_length is not None:
        current_user.preferred_session_length = updates.preferred_session_length
    if updates.dyslexia_font is not None:
        current_user.dyslexia_font = updates.dyslexia_font
    if updates.high_contrast is not None:
        current_user.high_contrast = updates.high_contrast
    if updates.reduce_animations is not None:
        current_user.reduce_animations = updates.reduce_animations
    
    await db.commit()
    await db.refresh(current_user)
    
    return UserResponse.model_validate(current_user)

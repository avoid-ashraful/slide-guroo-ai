"""
Authentication routes: registration, login, verification, password reset
"""
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, EmailStr
import logging

from database import get_db
from db_models import User
from auth_utils import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_verification_token,
    create_reset_token,
    get_user_by_email,
    get_user_by_username,
    get_current_user,
    VERIFICATION_TOKEN_EXPIRE_HOURS,
    RESET_TOKEN_EXPIRE_HOURS
)
from email_service import send_verification_email, send_password_reset_email, send_welcome_email

logger = logging.getLogger(__name__)
router = APIRouter()


# Pydantic models
class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str
    full_name: str | None = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    full_name: str | None
    is_verified: bool
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordReset(BaseModel):
    token: str
    new_password: str


class EmailVerification(BaseModel):
    token: str


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, db: AsyncSession = Depends(get_db)):
    """Register a new user"""

    # Check if email already exists
    existing_user = await get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Check if username already exists
    existing_username = await get_user_by_username(db, user_data.username)
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )

    # Create verification token
    verification_token = create_verification_token()
    token_expires = datetime.utcnow() + timedelta(hours=VERIFICATION_TOKEN_EXPIRE_HOURS)

    # Create new user
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=get_password_hash(user_data.password),
        full_name=user_data.full_name,
        verification_token=verification_token,
        verification_token_expires=token_expires
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    # Send verification email
    try:
        await send_verification_email(
            email=new_user.email,
            username=new_user.username,
            token=verification_token
        )
    except Exception as e:
        logger.error(f"Failed to send verification email: {str(e)}")
        # Don't fail registration if email fails

    return new_user


@router.post("/login", response_model=Token)
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    """Login user and return JWT token"""

    # Find user by email
    user = await get_user_by_email(db, user_data.email)

    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )

    # Update last login
    user.last_login = datetime.utcnow()
    await db.commit()

    # Create access token
    access_token = create_access_token(data={"sub": user.id})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/verify-email")
async def verify_email(verification: EmailVerification, db: AsyncSession = Depends(get_db)):
    """Verify user's email with token"""

    # Find user with this token
    result = await db.execute(
        select(User).filter(User.verification_token == verification.token)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification token"
        )

    # Check if token expired
    if user.verification_token_expires and user.verification_token_expires < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification token has expired"
        )

    # Verify user
    user.is_verified = True
    user.verification_token = None
    user.verification_token_expires = None

    await db.commit()

    # Send welcome email
    try:
        await send_welcome_email(user.email, user.username)
    except Exception as e:
        logger.error(f"Failed to send welcome email: {str(e)}")

    return {"message": "Email verified successfully"}


@router.post("/resend-verification")
async def resend_verification(email: EmailStr, db: AsyncSession = Depends(get_db)):
    """Resend verification email"""

    user = await get_user_by_email(db, email)

    if not user:
        # Don't reveal if email exists
        return {"message": "If the email exists, a verification link has been sent"}

    if user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already verified"
        )

    # Create new verification token
    verification_token = create_verification_token()
    token_expires = datetime.utcnow() + timedelta(hours=VERIFICATION_TOKEN_EXPIRE_HOURS)

    user.verification_token = verification_token
    user.verification_token_expires = token_expires

    await db.commit()

    # Send verification email
    try:
        await send_verification_email(user.email, user.username, verification_token)
    except Exception as e:
        logger.error(f"Failed to send verification email: {str(e)}")

    return {"message": "If the email exists, a verification link has been sent"}


@router.post("/forgot-password")
async def forgot_password(request: PasswordResetRequest, db: AsyncSession = Depends(get_db)):
    """Request password reset"""

    user = await get_user_by_email(db, request.email)

    if not user:
        # Don't reveal if email exists
        return {"message": "If the email exists, a password reset link has been sent"}

    # Create reset token
    reset_token = create_reset_token()
    token_expires = datetime.utcnow() + timedelta(hours=RESET_TOKEN_EXPIRE_HOURS)

    user.reset_token = reset_token
    user.reset_token_expires = token_expires

    await db.commit()

    # Send reset email
    try:
        await send_password_reset_email(user.email, user.username, reset_token)
    except Exception as e:
        logger.error(f"Failed to send password reset email: {str(e)}")

    return {"message": "If the email exists, a password reset link has been sent"}


@router.post("/reset-password")
async def reset_password(reset_data: PasswordReset, db: AsyncSession = Depends(get_db)):
    """Reset password with token"""

    # Find user with this token
    result = await db.execute(
        select(User).filter(User.reset_token == reset_data.token)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid reset token"
        )

    # Check if token expired
    if user.reset_token_expires and user.reset_token_expires < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reset token has expired"
        )

    # Update password
    user.hashed_password = get_password_hash(reset_data.new_password)
    user.reset_token = None
    user.reset_token_expires = None

    await db.commit()

    return {"message": "Password reset successfully"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return current_user


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "auth"}

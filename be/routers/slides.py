"""
API router for slide upload and processing
"""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
import os
import shutil
import logging
import re
from typing import Optional
import aiofiles
import uuid
from datetime import datetime

from models import SlideUploadResponse, Language, ErrorResponse
from services.lesson_generator import LessonGenerator
from services import lesson_service
from database import get_db
from db_models import User
from auth_utils import get_current_verified_user

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize lesson generator
lesson_generator = LessonGenerator()

# Get upload directory and size limit from env
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
MAX_UPLOAD_SIZE = int(os.getenv("MAX_UPLOAD_SIZE", str(50 * 1024 * 1024)))  # Default 50MB
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=SlideUploadResponse)
async def upload_slide(
    file: UploadFile = File(...),
    language: str = Form("en"),
    difficulty_level: str = Form("intermediate"),
    include_diagrams: bool = Form(True),
    current_user: User = Depends(get_current_verified_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload and process a slide/document file

    Args:
        file: PowerPoint, PDF, or Word document
        language: Target language (en/bn)
        difficulty_level: Difficulty level (beginner/intermediate/advanced)
        include_diagrams: Whether to generate diagrams

    Returns:
        Generated lesson
    """
    logger.info(f"Received file upload: {file.filename}")

    # Validate file type
    allowed_extensions = ['.ppt', '.pptx', '.pdf', '.docx', '.doc']
    file_ext = os.path.splitext(file.filename)[1].lower()

    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
        )

    # Read file content and validate size
    content = await file.read()
    file_size = len(content)

    logger.info(f"File size: {file_size} bytes (max: {MAX_UPLOAD_SIZE} bytes)")

    if file_size > MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {MAX_UPLOAD_SIZE // (1024*1024)}MB"
        )

    if file_size == 0:
        raise HTTPException(
            status_code=400,
            detail="File is empty"
        )

    # Create user-specific upload directory with sanitized user_id
    # Sanitize user_id to prevent path traversal attacks
    safe_user_id = re.sub(r'[^a-zA-Z0-9_-]', '', current_user.id)
    if not safe_user_id:
        raise HTTPException(
            status_code=500,
            detail="Invalid user ID format"
        )

    user_upload_dir = os.path.join(UPLOAD_DIR, safe_user_id)
    os.makedirs(user_upload_dir, exist_ok=True)

    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(user_upload_dir, unique_filename)

    try:
        # Save uploaded file
        async with aiofiles.open(file_path, 'wb') as out_file:
            await out_file.write(content)

        logger.info(f"Saved file to: {file_path} for user {current_user.username}")

        # Generate lesson
        lang_enum = Language.BANGLA if language == "bn" else Language.ENGLISH

        lesson = await lesson_generator.generate_from_file(
            file_path=file_path,
            language=lang_enum,
            difficulty_level=difficulty_level,
            include_diagrams=include_diagrams
        )

        # Save lesson to database
        await lesson_service.save_lesson(
            db=db,
            user_id=current_user.id,
            lesson=lesson,
            source_type="upload",
            source_file=file_path
        )

        return SlideUploadResponse(
            lesson_id=lesson.id,
            title=lesson.title,
            total_sections=len(lesson.sections),
            message="Lesson generated and saved successfully",
            lesson=lesson
        )

    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        # Clean up file if it was saved
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail="Unable to process file. Please ensure it's a valid document and try again.")

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "slides"}

"""
API router for slide upload and processing
"""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import os
import shutil
import logging
from typing import Optional
import aiofiles

from models import SlideUploadResponse, Language, ErrorResponse
from services.lesson_generator import LessonGenerator

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize lesson generator
lesson_generator = LessonGenerator()

# Get upload directory from env
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=SlideUploadResponse)
async def upload_slide(
    file: UploadFile = File(...),
    language: str = Form("en"),
    difficulty_level: str = Form("intermediate"),
    include_diagrams: bool = Form(True)
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

    # Save uploaded file
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    try:
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)

        logger.info(f"Saved file to: {file_path}")

        # Generate lesson
        lang_enum = Language.BANGLA if language == "bn" else Language.ENGLISH

        lesson = await lesson_generator.generate_from_file(
            file_path=file_path,
            language=lang_enum,
            difficulty_level=difficulty_level,
            include_diagrams=include_diagrams
        )

        return SlideUploadResponse(
            lesson_id=lesson.id,
            title=lesson.title,
            total_sections=len(lesson.sections),
            message="Lesson generated successfully",
            lesson=lesson
        )

    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "slides"}

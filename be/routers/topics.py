"""
API router for topic-based lesson generation
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from models import TopicRequest, TopicResponse, Language
from services.lesson_generator import LessonGenerator
from services import lesson_service
from database import get_db
from db_models import User
from auth_utils import get_current_verified_user

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize lesson generator
lesson_generator = LessonGenerator()

@router.post("/generate", response_model=TopicResponse)
async def generate_topic_lesson(
    request: TopicRequest,
    current_user: User = Depends(get_current_verified_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Generate lesson from a topic

    Args:
        request: Topic request with topic, language, and preferences

    Returns:
        Generated lesson
    """
    logger.info(f"Generating lesson for topic '{request.topic}' for user {current_user.username}")

    try:
        # Generate lesson
        lesson = await lesson_generator.generate_from_topic(
            topic=request.topic,
            language=request.language,
            difficulty_level=request.difficulty_level,
            include_diagrams=request.include_diagrams
        )

        # Save lesson to database
        await lesson_service.save_lesson(
            db=db,
            user_id=current_user.id,
            lesson=lesson,
            source_type="topic",
            source_topic=request.topic
        )

        return TopicResponse(
            lesson_id=lesson.id,
            lesson=lesson,
            message=f"Lesson on '{request.topic}' generated and saved successfully"
        )

    except Exception as e:
        logger.error(f"Error generating topic lesson: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating lesson: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "topics"}

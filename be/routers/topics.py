"""
API router for topic-based lesson generation
"""
from fastapi import APIRouter, HTTPException
import logging

from models import TopicRequest, TopicResponse, Language
from services.lesson_generator import LessonGenerator

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize lesson generator
lesson_generator = LessonGenerator()

@router.post("/generate", response_model=TopicResponse)
async def generate_topic_lesson(request: TopicRequest):
    """
    Generate lesson from a topic

    Args:
        request: Topic request with topic, language, and preferences

    Returns:
        Generated lesson
    """
    logger.info(f"Generating lesson for topic: {request.topic}")

    try:
        lesson = await lesson_generator.generate_from_topic(
            topic=request.topic,
            language=request.language,
            difficulty_level=request.difficulty_level,
            include_diagrams=request.include_diagrams
        )

        return TopicResponse(
            lesson_id=lesson.id,
            lesson=lesson,
            message=f"Lesson on '{request.topic}' generated successfully"
        )

    except Exception as e:
        logger.error(f"Error generating topic lesson: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating lesson: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "topics"}

"""
API router for interactive Q&A chat
"""
from fastapi import APIRouter, HTTPException
import logging
from typing import Dict

from models import ChatRequest, ChatResponse, Lesson
from services.lesson_generator import LessonGenerator

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize lesson generator
lesson_generator = LessonGenerator()

# In-memory storage for lessons (in production, use database)
lessons_store: Dict[str, Lesson] = {}

@router.post("/ask", response_model=ChatResponse)
async def ask_question(request: ChatRequest):
    """
    Ask a question about a lesson

    Args:
        request: Chat request with question and context

    Returns:
        AI-generated answer with related concepts
    """
    logger.info(f"Received question for lesson {request.lesson_id}: {request.question}")

    # In a real application, fetch lesson from database
    # For now, we'll create a simple context
    if request.lesson_id in lessons_store:
        lesson = lessons_store[request.lesson_id]
    else:
        # If lesson not in store, we'll still try to answer with provided context
        logger.warning(f"Lesson {request.lesson_id} not found in store, using provided context")
        if not request.context:
            raise HTTPException(
                status_code=404,
                detail="Lesson not found. Please provide context or regenerate the lesson."
            )

    try:
        # Get answer from lesson generator
        if request.lesson_id in lessons_store:
            answer_data = await lesson_generator.answer_question(
                lesson=lessons_store[request.lesson_id],
                question=request.question,
                language=request.language,
                conversation_history=[msg.dict() for msg in request.conversation_history]
            )
        else:
            # Use LLM service directly with provided context
            answer_data = await lesson_generator.llm_service.answer_question(
                question=request.question,
                context=request.context or "",
                conversation_history=[msg.dict() for msg in request.conversation_history],
                language=request.language.value
            )

        return ChatResponse(
            answer=answer_data.get("answer", ""),
            language=request.language,
            related_concepts=answer_data.get("related_concepts", []),
            additional_examples=answer_data.get("additional_examples", [])
        )

    except Exception as e:
        logger.error(f"Error answering question: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error answering question: {str(e)}")

@router.post("/store-lesson")
async def store_lesson(lesson: Lesson):
    """
    Store a lesson for later Q&A access

    Args:
        lesson: Lesson to store

    Returns:
        Success message
    """
    lessons_store[lesson.id] = lesson
    logger.info(f"Stored lesson: {lesson.id}")
    return {"message": "Lesson stored successfully", "lesson_id": lesson.id}

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "chat"}

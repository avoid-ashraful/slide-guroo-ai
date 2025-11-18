"""
API router for interactive Q&A chat
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from models import ChatRequest, ChatResponse, Lesson
from services.lesson_generator import LessonGenerator
from services import lesson_service, chat_history_service
from database import get_db
from db_models import User
from auth_utils import get_current_verified_user

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize lesson generator
lesson_generator = LessonGenerator()


@router.post("/ask", response_model=ChatResponse)
async def ask_question(
    request: ChatRequest,
    current_user: User = Depends(get_current_verified_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Ask a question about a lesson

    Args:
        request: Chat request with question and context
        current_user: Authenticated user
        db: Database session

    Returns:
        AI-generated answer with related concepts
    """
    logger.info(f"User {current_user.username} asking question about lesson {request.lesson_id}")

    try:
        # Fetch lesson from database
        user_lesson = await lesson_service.get_lesson_by_id(
            db=db,
            lesson_id=request.lesson_id,
            user_id=current_user.id
        )

        if not user_lesson:
            raise HTTPException(
                status_code=404,
                detail="Lesson not found or you don't have access to it"
            )

        # Reconstruct Lesson object from stored data
        lesson = Lesson(**user_lesson.lesson_data)

        # Get conversation history from database
        conversation_history = await chat_history_service.get_conversation_by_lesson(
            db=db,
            user_id=current_user.id,
            lesson_id=request.lesson_id
        )

        # Save user's question to database
        await chat_history_service.save_chat_message(
            db=db,
            user_id=current_user.id,
            role="user",
            content=request.question,
            lesson_id=request.lesson_id,
            context=request.context,
            language=request.language.value
        )

        # Get answer from lesson generator
        answer_data = await lesson_generator.answer_question(
            lesson=lesson,
            question=request.question,
            language=request.language,
            conversation_history=[msg.dict() for msg in conversation_history]
        )

        # Save AI's response to database
        await chat_history_service.save_chat_message(
            db=db,
            user_id=current_user.id,
            role="assistant",
            content=answer_data.get("answer", ""),
            lesson_id=request.lesson_id,
            related_concepts=answer_data.get("related_concepts", []),
            additional_examples=answer_data.get("additional_examples", []),
            language=request.language.value
        )

        return ChatResponse(
            answer=answer_data.get("answer", ""),
            language=request.language,
            related_concepts=answer_data.get("related_concepts", []),
            additional_examples=answer_data.get("additional_examples", [])
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error answering question: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error answering question: {str(e)}")


@router.get("/history/{lesson_id}")
async def get_chat_history(
    lesson_id: str,
    current_user: User = Depends(get_current_verified_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get chat history for a specific lesson

    Args:
        lesson_id: Lesson ID
        current_user: Authenticated user
        db: Database session

    Returns:
        Chat history
    """
    try:
        # Verify user has access to this lesson
        user_lesson = await lesson_service.get_lesson_by_id(
            db=db,
            lesson_id=lesson_id,
            user_id=current_user.id
        )

        if not user_lesson:
            raise HTTPException(
                status_code=404,
                detail="Lesson not found or you don't have access to it"
            )

        # Get conversation history
        messages = await chat_history_service.get_conversation_by_lesson(
            db=db,
            user_id=current_user.id,
            lesson_id=lesson_id
        )

        return {
            "lesson_id": lesson_id,
            "messages": [msg.dict() for msg in messages],
            "total": len(messages)
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching chat history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching chat history: {str(e)}")


@router.delete("/history/{lesson_id}")
async def delete_chat_history(
    lesson_id: str,
    current_user: User = Depends(get_current_verified_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete chat history for a specific lesson

    Args:
        lesson_id: Lesson ID
        current_user: Authenticated user
        db: Database session

    Returns:
        Success message
    """
    try:
        # Verify user has access to this lesson
        user_lesson = await lesson_service.get_lesson_by_id(
            db=db,
            lesson_id=lesson_id,
            user_id=current_user.id
        )

        if not user_lesson:
            raise HTTPException(
                status_code=404,
                detail="Lesson not found or you don't have access to it"
            )

        # Delete chat history
        count = await chat_history_service.delete_chat_history(
            db=db,
            user_id=current_user.id,
            lesson_id=lesson_id
        )

        return {
            "message": f"Deleted {count} messages",
            "lesson_id": lesson_id
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting chat history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting chat history: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "chat"}

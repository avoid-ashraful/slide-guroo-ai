"""
API router for user dashboard
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import List, Optional
import logging

from models import Language
from services import lesson_service, chat_history_service
from database import get_db
from db_models import User, UserLesson, ChatHistory
from auth_utils import get_current_verified_user

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/lessons")
async def get_user_lessons(
    skip: int = 0,
    limit: int = 20,
    source_type: Optional[str] = None,
    current_user: User = Depends(get_current_verified_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all lessons for the current user

    Args:
        skip: Number of lessons to skip (pagination)
        limit: Maximum number of lessons to return (max 100)
        source_type: Filter by source type ('upload' or 'topic')
        current_user: Authenticated user
        db: Database session

    Returns:
        List of user's lessons with metadata
    """
    # Enforce maximum pagination limit
    MAX_LIMIT = 100
    if limit > MAX_LIMIT:
        limit = MAX_LIMIT
    if skip < 0:
        skip = 0

    try:
        lessons = await lesson_service.get_user_lessons(
            db=db,
            user_id=current_user.id,
            skip=skip,
            limit=limit,
            source_type=source_type
        )

        # Get total count
        query = select(func.count(UserLesson.id)).filter(UserLesson.user_id == current_user.id)
        if source_type:
            query = query.filter(UserLesson.source_type == source_type)

        result = await db.execute(query)
        total = result.scalar()

        return {
            "lessons": [
                {
                    "id": lesson.id,
                    "title": lesson.title,
                    "source_type": lesson.source_type,
                    "source_topic": lesson.source_topic,
                    "source_file": lesson.source_file.split('/')[-1] if lesson.source_file else None,
                    "created_at": lesson.created_at.isoformat(),
                    "updated_at": lesson.updated_at.isoformat(),
                    "total_sections": len(lesson.lesson_data.get("sections", [])),
                    "language": lesson.lesson_data.get("language", "en")
                }
                for lesson in lessons
            ],
            "total": total,
            "skip": skip,
            "limit": limit
        }

    except Exception as e:
        logger.error(f"Error fetching user lessons: {str(e)}")
        raise HTTPException(status_code=500, detail="Unable to fetch lessons. Please try again later.")


@router.get("/lessons/{lesson_id}")
async def get_lesson_detail(
    lesson_id: str,
    current_user: User = Depends(get_current_verified_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get detailed information about a specific lesson

    Args:
        lesson_id: Lesson ID
        current_user: Authenticated user
        db: Database session

    Returns:
        Full lesson data
    """
    try:
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

        return {
            "id": user_lesson.id,
            "title": user_lesson.title,
            "source_type": user_lesson.source_type,
            "source_topic": user_lesson.source_topic,
            "source_file": user_lesson.source_file,
            "created_at": user_lesson.created_at.isoformat(),
            "updated_at": user_lesson.updated_at.isoformat(),
            "lesson": user_lesson.lesson_data
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching lesson detail: {str(e)}")
        raise HTTPException(status_code=500, detail="Unable to fetch lesson details. Please try again later.")


@router.delete("/lessons/{lesson_id}")
async def delete_lesson(
    lesson_id: str,
    current_user: User = Depends(get_current_verified_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a lesson and its associated chat history

    Args:
        lesson_id: Lesson ID
        current_user: Authenticated user
        db: Database session

    Returns:
        Success message
    """
    try:
        # Verify ownership
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

        # Delete associated chat history first
        chat_count = await chat_history_service.delete_chat_history(
            db=db,
            user_id=current_user.id,
            lesson_id=lesson_id
        )

        # Delete the lesson
        success = await lesson_service.delete_lesson(
            db=db,
            lesson_id=lesson_id,
            user_id=current_user.id
        )

        if not success:
            raise HTTPException(status_code=404, detail="Failed to delete lesson")

        return {
            "message": "Lesson deleted successfully",
            "lesson_id": lesson_id,
            "deleted_chat_messages": chat_count
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting lesson: {str(e)}")
        raise HTTPException(status_code=500, detail="Unable to delete lesson. Please try again later.")


@router.get("/stats")
async def get_user_stats(
    current_user: User = Depends(get_current_verified_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get user statistics

    Args:
        current_user: Authenticated user
        db: Database session

    Returns:
        User statistics (total lessons, total chats, etc.)
    """
    try:
        # Count total lessons
        lessons_result = await db.execute(
            select(func.count(UserLesson.id)).filter(UserLesson.user_id == current_user.id)
        )
        total_lessons = lessons_result.scalar()

        # Count lessons by source type
        upload_result = await db.execute(
            select(func.count(UserLesson.id)).filter(
                UserLesson.user_id == current_user.id,
                UserLesson.source_type == "upload"
            )
        )
        lessons_from_upload = upload_result.scalar()

        topic_result = await db.execute(
            select(func.count(UserLesson.id)).filter(
                UserLesson.user_id == current_user.id,
                UserLesson.source_type == "topic"
            )
        )
        lessons_from_topic = topic_result.scalar()

        # Count total chat messages
        chat_result = await db.execute(
            select(func.count(ChatHistory.id)).filter(ChatHistory.user_id == current_user.id)
        )
        total_chat_messages = chat_result.scalar()

        # Count user questions vs AI responses
        user_messages_result = await db.execute(
            select(func.count(ChatHistory.id)).filter(
                ChatHistory.user_id == current_user.id,
                ChatHistory.role == "user"
            )
        )
        total_questions = user_messages_result.scalar()

        # Get most recent lesson
        recent_lesson_result = await db.execute(
            select(UserLesson).filter(UserLesson.user_id == current_user.id)
            .order_by(desc(UserLesson.created_at))
            .limit(1)
        )
        recent_lesson = recent_lesson_result.scalar_one_or_none()

        return {
            "user": {
                "id": current_user.id,
                "username": current_user.username,
                "email": current_user.email,
                "is_verified": current_user.is_verified,
                "joined_at": current_user.created_at.isoformat()
            },
            "stats": {
                "total_lessons": total_lessons,
                "lessons_from_upload": lessons_from_upload,
                "lessons_from_topic": lessons_from_topic,
                "total_chat_messages": total_chat_messages,
                "total_questions_asked": total_questions
            },
            "recent_lesson": {
                "id": recent_lesson.id,
                "title": recent_lesson.title,
                "created_at": recent_lesson.created_at.isoformat()
            } if recent_lesson else None
        }

    except Exception as e:
        logger.error(f"Error fetching user stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Unable to fetch statistics. Please try again later.")


@router.get("/recent-activity")
async def get_recent_activity(
    limit: int = 10,
    current_user: User = Depends(get_current_verified_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get user's recent activity (recent lessons and chats)

    Args:
        limit: Maximum number of items to return (max 100)
        current_user: Authenticated user
        db: Database session

    Returns:
        Recent lessons and chat messages
    """
    # Enforce maximum pagination limit
    MAX_LIMIT = 100
    if limit > MAX_LIMIT:
        limit = MAX_LIMIT
    if limit < 0:
        limit = 10  # Reset to default if negative

    try:
        # Get recent lessons
        recent_lessons_result = await db.execute(
            select(UserLesson).filter(UserLesson.user_id == current_user.id)
            .order_by(desc(UserLesson.created_at))
            .limit(limit)
        )
        recent_lessons = recent_lessons_result.scalars().all()

        # Get recent chat messages
        recent_chats_result = await db.execute(
            select(ChatHistory).filter(ChatHistory.user_id == current_user.id)
            .order_by(desc(ChatHistory.created_at))
            .limit(limit)
        )
        recent_chats = recent_chats_result.scalars().all()

        return {
            "recent_lessons": [
                {
                    "id": lesson.id,
                    "title": lesson.title,
                    "source_type": lesson.source_type,
                    "created_at": lesson.created_at.isoformat()
                }
                for lesson in recent_lessons
            ],
            "recent_chats": [
                {
                    "id": chat.id,
                    "lesson_id": chat.lesson_id,
                    "role": chat.role,
                    "content": chat.content[:100] + "..." if len(chat.content) > 100 else chat.content,
                    "created_at": chat.created_at.isoformat()
                }
                for chat in recent_chats
            ]
        }

    except Exception as e:
        logger.error(f"Error fetching recent activity: {str(e)}")
        raise HTTPException(status_code=500, detail="Unable to fetch recent activity. Please try again later.")


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "dashboard"}

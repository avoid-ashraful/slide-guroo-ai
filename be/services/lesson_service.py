"""
Service for managing user lessons in database
"""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from db_models import UserLesson, User
from models import Lesson
import logging

logger = logging.getLogger(__name__)


async def save_lesson(
    db: AsyncSession,
    user_id: str,
    lesson: Lesson,
    source_type: str,
    source_file: Optional[str] = None,
    source_topic: Optional[str] = None
) -> UserLesson:
    """
    Save a lesson to database

    Args:
        db: Database session
        user_id: User ID
        lesson: Lesson object
        source_type: 'upload' or 'topic'
        source_file: File path if uploaded
        source_topic: Topic if generated

    Returns:
        Saved UserLesson object
    """
    user_lesson = UserLesson(
        id=lesson.id,
        user_id=user_id,
        lesson_data=lesson.dict(),
        title=lesson.title,
        subject=lesson.subject,
        difficulty_level=lesson.difficulty_level,
        source_type=source_type,
        source_file=source_file,
        source_topic=source_topic
    )

    db.add(user_lesson)
    await db.commit()
    await db.refresh(user_lesson)

    logger.info(f"Saved lesson {lesson.id} for user {user_id}")
    return user_lesson


async def get_user_lessons(
    db: AsyncSession,
    user_id: str,
    skip: int = 0,
    limit: int = 20
) -> List[UserLesson]:
    """
    Get all lessons for a user

    Args:
        db: Database session
        user_id: User ID
        skip: Number to skip (pagination)
        limit: Max number to return

    Returns:
        List of UserLesson objects
    """
    result = await db.execute(
        select(UserLesson)
        .filter(UserLesson.user_id == user_id)
        .order_by(desc(UserLesson.created_at))
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def get_lesson_by_id(
    db: AsyncSession,
    lesson_id: str,
    user_id: str
) -> Optional[UserLesson]:
    """
    Get a specific lesson by ID

    Args:
        db: Database session
        lesson_id: Lesson ID
        user_id: User ID (for ownership verification)

    Returns:
        UserLesson object or None
    """
    result = await db.execute(
        select(UserLesson)
        .filter(
            UserLesson.id == lesson_id,
            UserLesson.user_id == user_id
        )
    )
    return result.scalar_one_or_none()


async def delete_lesson(
    db: AsyncSession,
    lesson_id: str,
    user_id: str
) -> bool:
    """
    Delete a lesson

    Args:
        db: Database session
        lesson_id: Lesson ID
        user_id: User ID (for ownership verification)

    Returns:
        True if deleted, False if not found
    """
    lesson = await get_lesson_by_id(db, lesson_id, user_id)

    if not lesson:
        return False

    await db.delete(lesson)
    await db.commit()

    logger.info(f"Deleted lesson {lesson_id} for user {user_id}")
    return True

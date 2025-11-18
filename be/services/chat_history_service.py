"""
Service for managing chat history in database
"""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from db_models import ChatHistory
from models import ChatMessage
import logging

logger = logging.getLogger(__name__)


async def save_chat_message(
    db: AsyncSession,
    user_id: str,
    role: str,
    content: str,
    lesson_id: Optional[str] = None,
    context: Optional[str] = None,
    related_concepts: Optional[List[str]] = None,
    additional_examples: Optional[List[str]] = None,
    language: str = "en",
    attachment_path: Optional[str] = None,
    attachment_type: Optional[str] = None
) -> ChatHistory:
    """
    Save a chat message to database

    Args:
        db: Database session
        user_id: User ID
        role: 'user' or 'assistant'
        content: Message content
        lesson_id: Associated lesson ID (optional)
        context: Additional context
        related_concepts: List of related concepts
        additional_examples: List of examples
        language: Language code
        attachment_path: Path to attachment file
        attachment_type: Type of attachment (image/file)

    Returns:
        Saved ChatHistory object
    """
    chat_message = ChatHistory(
        user_id=user_id,
        lesson_id=lesson_id,
        role=role,
        content=content,
        context=context,
        related_concepts=related_concepts,
        additional_examples=additional_examples,
        language=language,
        has_attachment=bool(attachment_path),
        attachment_path=attachment_path,
        attachment_type=attachment_type
    )

    db.add(chat_message)
    await db.commit()
    await db.refresh(chat_message)

    logger.info(f"Saved chat message for user {user_id}")
    return chat_message


async def get_chat_history(
    db: AsyncSession,
    user_id: str,
    lesson_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 50
) -> List[ChatHistory]:
    """
    Get chat history for a user

    Args:
        db: Database session
        user_id: User ID
        lesson_id: Filter by lesson ID (optional)
        skip: Number to skip (pagination)
        limit: Max number to return

    Returns:
        List of ChatHistory objects
    """
    query = select(ChatHistory).filter(ChatHistory.user_id == user_id)

    if lesson_id:
        query = query.filter(ChatHistory.lesson_id == lesson_id)

    query = query.order_by(ChatHistory.created_at).offset(skip).limit(limit)

    result = await db.execute(query)
    return result.scalars().all()


async def get_conversation_by_lesson(
    db: AsyncSession,
    user_id: str,
    lesson_id: str
) -> List[ChatMessage]:
    """
    Get conversation for a specific lesson formatted as ChatMessage objects

    Args:
        db: Database session
        user_id: User ID
        lesson_id: Lesson ID

    Returns:
        List of ChatMessage objects
    """
    history = await get_chat_history(db, user_id, lesson_id)

    return [
        ChatMessage(
            role=msg.role,
            content=msg.content,
            timestamp=msg.created_at.isoformat()
        )
        for msg in history
    ]


async def delete_chat_history(
    db: AsyncSession,
    user_id: str,
    lesson_id: Optional[str] = None
) -> int:
    """
    Delete chat history for a user

    Args:
        db: Database session
        user_id: User ID
        lesson_id: Delete only for this lesson (optional)

    Returns:
        Number of messages deleted
    """
    query = select(ChatHistory).filter(ChatHistory.user_id == user_id)

    if lesson_id:
        query = query.filter(ChatHistory.lesson_id == lesson_id)

    result = await db.execute(query)
    messages = result.scalars().all()

    count = len(messages)
    for msg in messages:
        await db.delete(msg)

    await db.commit()

    logger.info(f"Deleted {count} chat messages for user {user_id}")
    return count

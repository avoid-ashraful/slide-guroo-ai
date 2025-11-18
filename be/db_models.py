"""
Database models for User and ChatHistory
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import uuid

class User(Base):
    """User model for authentication"""
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)

    # Email verification
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String, nullable=True)
    verification_token_expires = Column(DateTime, nullable=True)

    # Password reset
    reset_token = Column(String, nullable=True)
    reset_token_expires = Column(DateTime, nullable=True)

    # Account status
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    chat_histories = relationship("ChatHistory", back_populates="user", cascade="all, delete-orphan")
    lessons = relationship("UserLesson", back_populates="user", cascade="all, delete-orphan")


class UserLesson(Base):
    """Store user's generated lessons"""
    __tablename__ = "user_lessons"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)

    # Lesson data
    lesson_data = Column(JSON, nullable=False)  # Stores the entire lesson object
    title = Column(String, nullable=False)
    subject = Column(String, nullable=True)
    difficulty_level = Column(String, nullable=True)

    # Source information
    source_type = Column(String, nullable=False)  # 'upload' or 'topic'
    source_file = Column(String, nullable=True)  # File path if uploaded
    source_topic = Column(String, nullable=True)  # Topic if generated

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="lessons")
    chat_histories = relationship("ChatHistory", back_populates="lesson", cascade="all, delete-orphan")


class ChatHistory(Base):
    """Store user's chat history with AI"""
    __tablename__ = "chat_history"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    lesson_id = Column(String, ForeignKey("user_lessons.id"), nullable=True)

    # Message data
    role = Column(String, nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)

    # Additional context
    context = Column(Text, nullable=True)

    # Related concepts and examples (from AI response)
    related_concepts = Column(JSON, nullable=True)
    additional_examples = Column(JSON, nullable=True)

    # Attachments
    has_attachment = Column(Boolean, default=False)
    attachment_type = Column(String, nullable=True)  # 'image', 'file'
    attachment_path = Column(String, nullable=True)

    # Metadata
    language = Column(String, default="en")
    metadata = Column(JSON, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="chat_histories")
    lesson = relationship("UserLesson", back_populates="chat_histories")

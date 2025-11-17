"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

class Language(str, Enum):
    """Supported languages"""
    ENGLISH = "en"
    BANGLA = "bn"

class DiagramType(str, Enum):
    """Supported diagram types"""
    FLOWCHART = "flowchart"
    MINDMAP = "mindmap"
    TIMELINE = "timeline"
    TREE = "tree"
    NETWORK = "network"
    SEQUENCE = "sequence"

class LessonSection(BaseModel):
    """Individual lesson section"""
    id: str
    title: str
    content: str
    order: int
    diagram: Optional[str] = None  # Mermaid diagram code
    diagram_type: Optional[DiagramType] = None
    examples: List[str] = []
    key_points: List[str] = []

class Lesson(BaseModel):
    """Complete lesson structure"""
    id: str
    title: str
    description: str
    subject: str
    difficulty_level: str  # beginner, intermediate, advanced
    prerequisites: List[str] = []
    sections: List[LessonSection]
    summary: str
    language: Language = Language.ENGLISH
    created_at: str

class SlideUploadResponse(BaseModel):
    """Response after slide upload and processing"""
    lesson_id: str
    title: str
    total_sections: int
    message: str
    lesson: Lesson

class TopicRequest(BaseModel):
    """Request to generate lesson from topic"""
    topic: str = Field(..., description="Topic to learn about")
    language: Language = Field(Language.ENGLISH, description="Preferred language")
    difficulty_level: Optional[str] = Field("intermediate", description="Difficulty level")
    include_diagrams: bool = Field(True, description="Whether to generate diagrams")

class TopicResponse(BaseModel):
    """Response for topic-based lesson generation"""
    lesson_id: str
    lesson: Lesson
    message: str

class ChatMessage(BaseModel):
    """Chat message structure"""
    role: str  # user, assistant
    content: str
    timestamp: Optional[str] = None

class ChatRequest(BaseModel):
    """Request for chat/Q&A"""
    lesson_id: str
    question: str
    language: Language = Field(Language.ENGLISH)
    context: Optional[str] = None  # Additional context from the lesson
    conversation_history: List[ChatMessage] = []

class ChatResponse(BaseModel):
    """Response for chat/Q&A"""
    answer: str
    language: Language
    related_concepts: List[str] = []
    additional_examples: List[str] = []

class DiagramRequest(BaseModel):
    """Request to generate a diagram"""
    concept: str = Field(..., description="Concept to visualize")
    diagram_type: Optional[DiagramType] = None
    context: Optional[str] = None

class DiagramResponse(BaseModel):
    """Response with generated diagram"""
    diagram_code: str  # Mermaid code
    diagram_type: DiagramType
    explanation: str

class ErrorResponse(BaseModel):
    """Error response"""
    error: str
    details: Optional[str] = None
    code: str

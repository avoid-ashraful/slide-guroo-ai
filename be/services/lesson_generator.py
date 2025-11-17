"""
Main lesson generation service
Orchestrates content extraction, LLM processing, and diagram generation
"""
import logging
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from services.content_extractor import ContentExtractor
from services.llm_service import LLMService
from services.diagram_service import DiagramService
from models import Lesson, LessonSection, Language, DiagramType

logger = logging.getLogger(__name__)

class LessonGenerator:
    """Main service for generating comprehensive lessons"""

    def __init__(self):
        self.content_extractor = ContentExtractor()
        self.llm_service = LLMService()
        self.diagram_service = DiagramService()

    async def generate_from_file(
        self,
        file_path: str,
        language: Language = Language.ENGLISH,
        difficulty_level: str = "intermediate",
        include_diagrams: bool = True
    ) -> Lesson:
        """
        Generate lesson from uploaded file (PPT, PDF, DOCX)

        Args:
            file_path: Path to uploaded file
            language: Target language
            difficulty_level: Difficulty level
            include_diagrams: Whether to generate diagrams

        Returns:
            Complete Lesson object
        """
        logger.info(f"Generating lesson from file: {file_path}")

        # Step 1: Extract content from file
        extracted_content = self.content_extractor.extract_from_file(file_path)
        content_summary = self.content_extractor.get_summary(extracted_content)

        # Step 2: Generate lesson structure using LLM
        lesson_data = await self.llm_service.generate_lesson_structure(
            content=content_summary,
            title=extracted_content['title'],
            language=language.value,
            difficulty_level=difficulty_level
        )

        # Step 3: Generate diagrams for sections that need them
        sections = []
        for idx, section_data in enumerate(lesson_data.get('sections', [])):
            section_id = str(uuid.uuid4())

            diagram_code = None
            diagram_type_enum = None

            if include_diagrams and section_data.get('needs_diagram', False):
                try:
                    diagram_type_str = section_data.get('diagram_type', 'flowchart')
                    diagram_description = section_data.get('diagram_description', '')

                    diagram_code = await self.diagram_service.enhance_section_with_diagram(
                        section_title=section_data['title'],
                        section_content=section_data['content'],
                        diagram_description=diagram_description,
                        diagram_type=diagram_type_str
                    )

                    # Map to enum
                    diagram_type_map = {
                        'flowchart': DiagramType.FLOWCHART,
                        'mindmap': DiagramType.MINDMAP,
                        'timeline': DiagramType.TIMELINE,
                        'tree': DiagramType.TREE,
                        'network': DiagramType.NETWORK,
                        'sequence': DiagramType.SEQUENCE
                    }
                    diagram_type_enum = diagram_type_map.get(diagram_type_str, DiagramType.FLOWCHART)

                except Exception as e:
                    logger.error(f"Error generating diagram for section {section_id}: {str(e)}")

            section = LessonSection(
                id=section_id,
                title=section_data['title'],
                content=section_data['content'],
                order=section_data.get('order', idx + 1),
                diagram=diagram_code,
                diagram_type=diagram_type_enum,
                examples=section_data.get('examples', []),
                key_points=section_data.get('key_points', [])
            )
            sections.append(section)

        # Step 4: Create complete lesson object
        lesson = Lesson(
            id=str(uuid.uuid4()),
            title=lesson_data.get('title', extracted_content['title']),
            description=lesson_data.get('description', ''),
            subject=lesson_data.get('subject', 'General'),
            difficulty_level=difficulty_level,
            prerequisites=lesson_data.get('prerequisites', []),
            sections=sections,
            summary=lesson_data.get('summary', ''),
            language=language,
            created_at=datetime.utcnow().isoformat()
        )

        logger.info(f"Successfully generated lesson: {lesson.id}")
        return lesson

    async def generate_from_topic(
        self,
        topic: str,
        language: Language = Language.ENGLISH,
        difficulty_level: str = "intermediate",
        include_diagrams: bool = True
    ) -> Lesson:
        """
        Generate lesson from topic query

        Args:
            topic: Topic to generate lesson about
            language: Target language
            difficulty_level: Difficulty level
            include_diagrams: Whether to generate diagrams

        Returns:
            Complete Lesson object
        """
        logger.info(f"Generating lesson for topic: {topic}")

        # Step 1: Generate comprehensive content for the topic
        topic_content = await self.llm_service.generate_topic_content(
            topic=topic,
            language=language.value,
            difficulty_level=difficulty_level
        )

        # Step 2: Generate structured lesson from the content
        lesson_data = await self.llm_service.generate_lesson_structure(
            content=topic_content,
            title=topic,
            language=language.value,
            difficulty_level=difficulty_level
        )

        # Step 3: Generate diagrams for sections that need them
        sections = []
        for idx, section_data in enumerate(lesson_data.get('sections', [])):
            section_id = str(uuid.uuid4())

            diagram_code = None
            diagram_type_enum = None

            if include_diagrams and section_data.get('needs_diagram', False):
                try:
                    diagram_type_str = section_data.get('diagram_type', 'flowchart')
                    diagram_description = section_data.get('diagram_description', '')

                    diagram_code = await self.diagram_service.enhance_section_with_diagram(
                        section_title=section_data['title'],
                        section_content=section_data['content'],
                        diagram_description=diagram_description,
                        diagram_type=diagram_type_str
                    )

                    # Map to enum
                    diagram_type_map = {
                        'flowchart': DiagramType.FLOWCHART,
                        'mindmap': DiagramType.MINDMAP,
                        'timeline': DiagramType.TIMELINE,
                        'tree': DiagramType.TREE,
                        'network': DiagramType.NETWORK,
                        'sequence': DiagramType.SEQUENCE
                    }
                    diagram_type_enum = diagram_type_map.get(diagram_type_str, DiagramType.FLOWCHART)

                except Exception as e:
                    logger.error(f"Error generating diagram for section {section_id}: {str(e)}")

            section = LessonSection(
                id=section_id,
                title=section_data['title'],
                content=section_data['content'],
                order=section_data.get('order', idx + 1),
                diagram=diagram_code,
                diagram_type=diagram_type_enum,
                examples=section_data.get('examples', []),
                key_points=section_data.get('key_points', [])
            )
            sections.append(section)

        # Step 4: Create complete lesson object
        lesson = Lesson(
            id=str(uuid.uuid4()),
            title=lesson_data.get('title', topic),
            description=lesson_data.get('description', f'Comprehensive lesson about {topic}'),
            subject=lesson_data.get('subject', 'General'),
            difficulty_level=difficulty_level,
            prerequisites=lesson_data.get('prerequisites', []),
            sections=sections,
            summary=lesson_data.get('summary', ''),
            language=language,
            created_at=datetime.utcnow().isoformat()
        )

        logger.info(f"Successfully generated lesson: {lesson.id}")
        return lesson

    async def answer_question(
        self,
        lesson: Lesson,
        question: str,
        language: Language = Language.ENGLISH,
        conversation_history: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Answer student question about a lesson

        Args:
            lesson: The lesson context
            question: Student's question
            language: Response language
            conversation_history: Previous conversation

        Returns:
            Answer dictionary
        """
        # Build context from lesson
        context_parts = [
            f"Lesson: {lesson.title}",
            f"Description: {lesson.description}",
            "\nKey Concepts:"
        ]

        for section in lesson.sections:
            context_parts.append(f"\n{section.title}")
            context_parts.append(section.content[:500])  # First 500 chars

        context = "\n".join(context_parts)

        # Get answer from LLM
        answer_data = await self.llm_service.answer_question(
            question=question,
            context=context,
            conversation_history=conversation_history or [],
            language=language.value
        )

        return answer_data

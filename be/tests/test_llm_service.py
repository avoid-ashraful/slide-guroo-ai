"""
Tests for LLM Service
"""
import pytest
from services.llm_service import LLMService

@pytest.mark.asyncio
async def test_llm_service_initialization():
    """Test that LLM service initializes correctly"""
    service = LLMService()
    assert service.provider == "gemini"
    assert service.api_key is not None
    assert service.model == "gemini-2.0-flash"

@pytest.mark.asyncio
async def test_generate_completion():
    """Test basic completion generation"""
    service = LLMService()

    prompt = "Explain photosynthesis in one sentence."
    system_prompt = "You are a helpful science teacher."

    response = await service.generate_completion(
        prompt=prompt,
        system_prompt=system_prompt,
        temperature=0.7,
        max_tokens=100
    )

    assert response is not None
    assert len(response) > 0
    assert isinstance(response, str)

@pytest.mark.asyncio
async def test_generate_lesson_structure():
    """Test lesson structure generation"""
    service = LLMService()

    content = """
    Photosynthesis is the process plants use to convert light energy into chemical energy.
    """
    title = "Photosynthesis Basics"

    lesson = await service.generate_lesson_structure(
        content=content,
        title=title,
        language="en",
        difficulty_level="beginner"
    )

    assert lesson is not None
    assert "title" in lesson
    assert "sections" in lesson
    assert isinstance(lesson["sections"], list)
    assert len(lesson["sections"]) > 0

@pytest.mark.asyncio
async def test_answer_question():
    """Test question answering"""
    service = LLMService()

    question = "What is photosynthesis?"
    context = "Photosynthesis is a process used by plants to convert light into energy."

    answer = await service.answer_question(
        question=question,
        context=context,
        conversation_history=[],
        language="en"
    )

    assert answer is not None
    assert "answer" in answer
    assert len(answer["answer"]) > 0

@pytest.mark.asyncio
async def test_generate_topic_content():
    """Test topic content generation"""
    service = LLMService()

    topic = "Photosynthesis"

    content = await service.generate_topic_content(
        topic=topic,
        language="en",
        difficulty_level="intermediate"
    )

    assert content is not None
    assert len(content) > 100
    assert isinstance(content, str)
    assert "photosynthesis" in content.lower()

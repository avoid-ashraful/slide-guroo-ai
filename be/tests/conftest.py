"""
Pytest configuration and fixtures
"""
import pytest
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Set test environment variables
os.environ["LLM_PROVIDER"] = "gemini"
os.environ["GOOGLE_API_KEY"] = "AIzaSyB8b-F2FDwA9hAd39RZP-GoSRGo5k-t0xk"
os.environ["GEMINI_MODEL"] = "gemini-2.0-flash"
os.environ["HOST"] = "0.0.0.0"
os.environ["PORT"] = "8000"
os.environ["UPLOAD_DIR"] = "./test_uploads"

@pytest.fixture
def test_upload_dir(tmp_path):
    """Create temporary upload directory for tests"""
    upload_dir = tmp_path / "uploads"
    upload_dir.mkdir()
    return upload_dir

@pytest.fixture
def sample_text_content():
    """Sample text content for testing"""
    return """
    Photosynthesis

    Photosynthesis is the process by which plants use sunlight, water, and carbon dioxide
    to create oxygen and energy in the form of sugar.

    The chemical equation is:
    6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂

    This process occurs in the chloroplasts of plant cells.
    """

@pytest.fixture
def sample_lesson_data():
    """Sample lesson data for testing"""
    return {
        "title": "Photosynthesis",
        "description": "Learn about the process of photosynthesis",
        "subject": "Biology",
        "difficulty_level": "intermediate",
        "prerequisites": ["Basic chemistry", "Plant biology"],
        "sections": [
            {
                "title": "Introduction",
                "content": "What is photosynthesis?",
                "order": 1,
                "needs_diagram": True,
                "diagram_type": "flowchart",
                "diagram_description": "Show the photosynthesis process",
                "examples": ["Example 1"],
                "key_points": ["Point 1"]
            }
        ],
        "summary": "Photosynthesis is essential for life"
    }

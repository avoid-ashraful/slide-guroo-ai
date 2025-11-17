"""
API Integration Tests
"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_slides_health():
    """Test slides router health"""
    response = client.get("/api/slides/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_topics_health():
    """Test topics router health"""
    response = client.get("/api/topics/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_chat_health():
    """Test chat router health"""
    response = client.get("/api/chat/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_diagrams_health():
    """Test diagrams router health"""
    response = client.get("/api/diagrams/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

@pytest.mark.asyncio
async def test_topic_generation():
    """Test topic generation endpoint"""
    response = client.post(
        "/api/topics/generate",
        json={
            "topic": "Test Topic",
            "language": "en",
            "difficulty_level": "beginner",
            "include_diagrams": False
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "lesson_id" in data
    assert "lesson" in data
    assert data["lesson"]["title"] is not None

@pytest.mark.asyncio
async def test_diagram_generation():
    """Test diagram generation endpoint"""
    response = client.post(
        "/api/diagrams/generate",
        json={
            "concept": "Simple Process",
            "diagram_type": "flowchart",
            "context": "Test context"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "diagram_code" in data
    assert "diagram_type" in data
    assert len(data["diagram_code"]) > 0

"""
Tests for Content Extractor
"""
import pytest
import os
from pathlib import Path
from services.content_extractor import ContentExtractor

def test_content_extractor_initialization():
    """Test that content extractor initializes correctly"""
    extractor = ContentExtractor()
    assert extractor is not None
    assert len(extractor.supported_formats) > 0
    assert '.pptx' in extractor.supported_formats
    assert '.pdf' in extractor.supported_formats

def test_unsupported_format():
    """Test that unsupported formats raise error"""
    extractor = ContentExtractor()

    with pytest.raises(ValueError):
        extractor.extract_from_file("test.xyz")

def test_get_summary(sample_lesson_data):
    """Test summary generation"""
    extractor = ContentExtractor()

    # Create mock extracted content
    extracted_content = {
        'title': 'Test Lesson',
        'slides': [
            {
                'slide_number': 1,
                'title': 'Introduction',
                'content': ['This is slide content'],
                'notes': 'These are notes'
            }
        ],
        'source_type': 'presentation'
    }

    summary = extractor.get_summary(extracted_content)

    assert summary is not None
    assert len(summary) > 0
    assert 'Introduction' in summary

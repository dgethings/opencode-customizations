#!/usr/bin/env python3
"""
Pytest fixtures for youtube-obsidian tests.

This module provides reusable fixtures for test data generation,
API mocking, and common test utilities following pytest best practices.
"""

import json
import os
import tempfile
from typing import Any, Dict
from unittest.mock import Mock

import pytest
import requests_mock
from pytest_mock import MockerFixture


# =============================================================================
# FIXTURE: Sample Metadata Factory
# =============================================================================


@pytest.fixture
def sample_metadata() -> Dict[str, Any]:
    """Factory for generating sample video metadata.

    Returns a dictionary with typical YouTube video metadata structure.
    Override fields in tests using dict.update() or dictionary literals.

    Example:
        metadata = sample_metadata()
        metadata['title'] = 'Custom Title'
    """
    return {
        "title": "Test Video: Python Tutorial",
        "description": "Learn Python programming from scratch",
        "tags": ["python", "programming", "tutorial"],
    }


@pytest.fixture
def sample_metadata_empty() -> Dict[str, Any]:
    """Factory for empty metadata (edge case testing)."""
    return {
        "title": "",
        "description": "",
        "tags": [],
    }


@pytest.fixture
def sample_metadata_special_chars() -> Dict[str, Any]:
    """Factory for metadata with special characters (edge case testing)."""
    return {
        "title": 'Video: "Test" & Special <Chars>',
        "description": "Description with /\\|?* special chars",
        "tags": ["tag-with-dash", "tag_with_underscore"],
    }


# =============================================================================
# FIXTURE: Sample Transcript Factory
# =============================================================================


@pytest.fixture
def sample_transcript() -> str:
    """Factory for generating sample transcript text.

    Returns a realistic transcript with capitalized words
    for tag generation testing.
    """
    return """Welcome to this Python programming tutorial.
We'll cover Data Structures and Object Oriented Programming.
Machine Learning is an exciting field in software development.
API integration is essential for modern web applications.
Cloud deployment using Docker and Kubernetes."""


@pytest.fixture
def sample_transcript_empty() -> str:
    """Empty transcript for edge case testing."""
    return ""


@pytest.fixture
def sample_transcript_very_long() -> str:
    """Very long transcript for stress testing."""
    words = ["word" + str(i) for i in range(1000)]
    return " ".join(words)


@pytest.fixture
def sample_transcript_special_chars() -> str:
    """Transcript with special characters and unicode."""
    return """Hello World! @#$%^&*()
Special chars: <>&"'"
Unicode: café, naïve, 日本語
Emoji: 🎉 🔥 ❤️"""


@pytest.fixture
def sample_transcript_no_caps() -> str:
    """Transcript with no capitalized words (edge case)."""
    return "this is a transcript with no capital words at all just lowercase text"


# =============================================================================
# FIXTURE: YouTube API Response Factory
# =============================================================================


@pytest.fixture
def youtube_api_response(sample_metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Factory for generating YouTube API response structure.

    Returns a mock response matching YouTube Data API v3 format.
    """
    return {
        "items": [
            {
                "snippet": sample_metadata,
            }
        ]
    }


@pytest.fixture
def youtube_api_response_empty() -> Dict[str, Any]:
    """Empty YouTube API response (video not found)."""
    return {"items": []}


@pytest.fixture
def youtube_api_response_malformed() -> Dict[str, Any]:
    """Malformed YouTube API response (missing required fields)."""
    return {
        "items": [
            {
                "id": "test123",
                # Missing 'snippet' field
            }
        ]
    }


# =============================================================================
# FIXTURE: Transcript API Mock Factory
# =============================================================================


@pytest.fixture
def mock_transcript_entry_factory():
    """Factory for creating mock transcript entry objects.

    Returns a function that creates Mock objects with
    text, start, and duration attributes.
    """

    def _create_entry(text: str, start: float = 0.0, duration: float = 1.0):
        entry = Mock()
        entry.text = text
        entry.start = start
        entry.duration = duration
        return entry

    return _create_entry


@pytest.fixture
def mock_transcript_list(mock_transcript_entry_factory):
    """Factory for creating mock transcript list.

    Returns a list of Mock transcript entries.
    """
    return [
        mock_transcript_entry_factory("Hello", 0.0, 1.0),
        mock_transcript_entry_factory("World", 1.0, 1.0),
        mock_transcript_entry_factory("Python", 2.0, 1.0),
    ]


# =============================================================================
# FIXTURE: Temporary Directory for File Operations
# =============================================================================


@pytest.fixture
def temp_vault_path():
    """Create temporary directory for vault file operations.

    Yields a temporary directory path that is automatically
    cleaned up after the test.

    Example:
        def test_create_file(temp_vault_path):
            file_path = os.path.join(temp_vault_path, "test.md")
            # ... test logic ...
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


# =============================================================================
# FIXTURE: Environment Variables
# =============================================================================


@pytest.fixture
def mock_env_vars(monkeypatch):
    """Factory for mocking environment variables.

    Returns a function that sets environment variables
    and provides cleanup.

    Example:
        def test_with_env(mock_env_vars):
            mock_env_vars({
                'YOUTUBE_API_KEY': 'fake-key',
                'VAULT_PATH': '/tmp/vault'
            })
    """

    def _set_env(env_vars: Dict[str, str]):
        for key, value in env_vars.items():
            monkeypatch.setenv(key, value)

    return _set_env


# =============================================================================
# FIXTURE: HTTP Error Scenarios
# =============================================================================


@pytest.fixture
def mock_timeout_error():
    """Factory for creating timeout error mocks."""
    from requests.exceptions import Timeout

    return Timeout("Request timed out after 30 seconds")


@pytest.fixture
def mock_connection_error():
    """Factory for creating connection error mocks."""
    from requests.exceptions import ConnectionError

    return ConnectionError("Failed to establish connection")


# =============================================================================
# FIXTURE: Sample URLs
# =============================================================================


@pytest.fixture
def valid_youtube_urls():
    """List of valid YouTube URL formats for testing."""
    return [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtu.be/dQw4w9WgXcQ",
        "https://www.youtube.com/embed/dQw4w9WgXcQ",
        "https://www.youtube.com/v/dQw4w9WgXcQ",
        "dQw4w9WgXcQ",  # Just the ID
    ]


@pytest.fixture
def invalid_youtube_urls():
    """List of invalid YouTube URLs for error testing."""
    return [
        "https://example.com/not-a-youtube-url",
        "https://youtube.com/watch?v=invalid_too_short",
        "not-a-url-at-all",
        "",
    ]


# =============================================================================
# FIXTURE: Tag Generation Test Data
# =============================================================================


@pytest.fixture
def tag_generation_test_cases():
    """Comprehensive test cases for tag generation."""
    return [
        {
            "name": "Empty input",
            "title": "",
            "description": "",
            "transcript": "",
            "youtube_tags": [],
            "expected_count": 0,
        },
        {
            "name": "No capitalized words",
            "title": "no caps here",
            "description": "all lowercase text",
            "transcript": "nothing capitalized at all",
            "youtube_tags": [],
            "expected_count": 0,
        },
        {
            "name": "Only tech terms",
            "title": "no caps",
            "description": "all lowercase text about python and javascript",
            "transcript": "development and programming",
            "youtube_tags": [],
            "expected_count": 3,  # python, javascript, programming
        },
        {
            "name": "Mixed sources",
            "title": "Python Tutorial",
            "description": "Learn Machine Learning",
            "transcript": "API development",
            "youtube_tags": ["coding", "tutorial"],
            "expected_count": 5,  # coding, tutorial, python, machine learning, api
        },
        {
            "name": "Too many tags",
            "title": "Title",
            "description": "Description",
            "transcript": " ".join([f"Tag{i}" for i in range(20)]),
            "youtube_tags": [f"tag{i}" for i in range(20)],
            "expected_count": 15,  # Limited to 15
        },
    ]


# =============================================================================
# FIXTURE: Filename Sanitization Test Data
# =============================================================================


@pytest.fixture
def filename_sanitization_test_cases():
    """Comprehensive test cases for filename sanitization."""
    return [
        {
            "name": "Special chars",
            "input": 'Test: "File" <Name>',
            "expected": "Test File Name",
        },
        {
            "name": "Slashes",
            "input": "Test/File/Name\\Backslash",
            "expected": "TestFileNameBackslash",
        },
        {
            "name": "All special chars",
            "input": 'Test|?*Name<>:"/\\',
            "expected": "TestName",
        },
        {
            "name": "Empty",
            "input": "",
            "expected": "video",
        },
        {
            "name": "Very long",
            "input": "A" * 150,
            "expected": "A" * 97 + "...",
        },
        {
            "name": "Exactly 100 chars",
            "input": "A" * 100,
            "expected": "A" * 100,
        },
        {
            "name": "Trailing spaces",
            "input": "  Test  Name  ",
            "expected": "Test  Name",
        },
        {
            "name": "Unicode chars",
            "input": "日本語 中国語 🎉",
            "expected": "日本語 中国語 🎉",
        },
    ]


# =============================================================================
# PYTEST HOOKS: Custom markers
# =============================================================================


def pytest_configure(config):
    """Configure custom pytest markers for test prioritization."""
    config.addinivalue_line(
        "markers", "p0: Critical priority tests (revenue, security, data integrity)"
    )
    config.addinivalue_line(
        "markers", "p1: High priority tests (core user journeys, frequent features)"
    )
    config.addinivalue_line(
        "markers", "p2: Medium priority tests (edge cases, less critical features)"
    )
    config.addinivalue_line(
        "markers", "p3: Low priority tests (nice-to-have, rarely used)"
    )
    config.addinivalue_line("markers", "slow: Tests that take longer than 1 second")
    config.addinivalue_line(
        "markers", "integration: Integration tests (require external services)"
    )
    config.addinivalue_line("markers", "unit: Unit tests (no external dependencies)")

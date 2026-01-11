#!/usr/bin/env python3
import os
import sys
import json

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "skills",
        "youtube-obsidian",
        "scripts",
    ),
)

try:
    import requests_mock
except ImportError:
    print(
        "Error: requests-mock module not found. Install with: pip install requests-mock"
    )
    sys.exit(1)

import pytest

from get_youtube_data import (
    extract_video_id,
    get_video_metadata,
    get_transcript,
    generate_tags,
    sanitize_filename,
    create_obsidian_note,
)


class TestExtractVideoId:
    def test_extract_from_standard_watch_url(self):
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        result = extract_video_id(url)
        assert result == "dQw4w9WgXcQ"

    def test_extract_from_short_url(self):
        url = "https://youtu.be/dQw4w9WgXcQ"
        result = extract_video_id(url)
        assert result == "dQw4w9WgXcQ"

    def test_extract_from_embed_url(self):
        url = "https://www.youtube.com/embed/dQw4w9WgXcQ"
        result = extract_video_id(url)
        assert result == "dQw4w9WgXcQ"

    def test_extract_from_v_url(self):
        url = "https://www.youtube.com/v/dQw4w9WgXcQ"
        result = extract_video_id(url)
        assert result == "dQw4w9WgXcQ"

    def test_extract_from_video_id_only(self):
        url = "dQw4w9WgXcQ"
        result = extract_video_id(url)
        assert result == "dQw4w9WgXcQ"

    def test_extract_invalid_url(self):
        url = "https://example.com/not-a-youtube-url"
        with pytest.raises(ValueError, match="Could not extract video ID"):
            extract_video_id(url)


class TestSanitizeFilename:
    def test_remove_invalid_chars(self):
        filename = 'Test: "File" <Name>'
        result = sanitize_filename(filename)
        assert result == "Test File Name"

    def test_remove_slashes_and_backslashes(self):
        filename = "Test/File/Name\\Backslash"
        result = sanitize_filename(filename)
        assert result == "TestFileNameBackslash"

    def test_remove_special_chars(self):
        filename = "Test|?*Name"
        result = sanitize_filename(filename)
        assert result == "TestName"

    def test_truncate_long_title(self):
        filename = "A" * 150
        result = sanitize_filename(filename)
        assert len(result) == 100
        assert result.endswith("...")

    def test_empty_title_returns_default(self):
        filename = ""
        result = sanitize_filename(filename)
        assert result == "video"


class TestGenerateTags:
    def test_generate_from_youtube_tags(self):
        tags = generate_tags(
            "Python Tutorial",
            "Learn Python",
            "python programming",
            ["python", "coding"],
        )
        assert "python" in tags
        assert "coding" in tags

    def test_generate_from_capitalized_words(self):
        tags = generate_tags(
            "Machine Learning With Python", "Learn ML", "machine learning"
        )
        assert "machine learning" in tags or "machine" in tags
        assert len(tags) <= 15

    def test_generate_from_tech_terms(self):
        tags = generate_tags(
            "Python API Development", "API Tutorial", "api development python"
        )
        assert "api" in tags
        assert "python" in tags

    def test_no_duplicate_tags(self):
        tags = generate_tags(
            "Python Tutorial",
            "Learn Python",
            "python programming",
            ["python", "python"],
        )
        assert len([t for t in tags if t == "python"]) == 1

    def test_limit_to_15_tags(self):
        youtube_tags = ["tag" + str(i) for i in range(20)]
        tags = generate_tags("Title", "Description", "Transcript", youtube_tags)
        assert len(tags) <= 15


class TestCreateObsidianNote:
    def test_creates_valid_frontmatter(self):
        metadata = {
            "title": "Test Video",
            "description": "Test Description",
            "tags": ["test", "video"],
        }
        note, filename = create_obsidian_note(
            "test123",
            "https://youtube.com/watch?v=test123",
            metadata,
            "Test transcript",
            "Test summary",
        )
        assert "---" in note
        assert "title: Test Video" in note
        assert "youtube_id: test123" in note

    def test_includes_user_summary(self):
        metadata = {
            "title": "Test Video",
            "description": "Test Description",
            "tags": [],
        }
        note, filename = create_obsidian_note(
            "test123",
            "https://youtube.com/watch?v=test123",
            metadata,
            "Test transcript",
            "My summary",
        )
        assert "## Summary" in note
        assert "My summary" in note

    def test_includes_user_comments_when_provided(self):
        metadata = {
            "title": "Test Video",
            "description": "Test Description",
            "tags": [],
        }
        note, filename = create_obsidian_note(
            "test123",
            "https://youtube.com/watch?v=test123",
            metadata,
            "Test transcript",
            "My summary",
            "My comments",
        )
        assert "## Notes/Comments" in note
        assert "My comments" in note

    def test_includes_description(self):
        metadata = {
            "title": "Test Video",
            "description": "This is a test description",
            "tags": [],
        }
        note, filename = create_obsidian_note(
            "test123",
            "https://youtube.com/watch?v=test123",
            metadata,
            "Test transcript",
            "My summary",
        )
        assert "## Description" in note
        assert "This is a test description" in note


class TestGetVideoMetadata:
    def test_fetch_metadata_success(self, requests_mock):
        mock_response = {
            "items": [
                {
                    "snippet": {
                        "title": "Test Video",
                        "description": "Test Description",
                        "tags": ["test", "video"],
                    }
                }
            ]
        }
        requests_mock.get(
            "https://www.googleapis.com/youtube/v3/videos", json=mock_response
        )
        result = get_video_metadata("test123", "fake_api_key")
        assert result["title"] == "Test Video"
        assert result["description"] == "Test Description"
        assert result["tags"] == ["test", "video"]

    def test_video_not_found(self, requests_mock):
        mock_response = {"items": []}
        requests_mock.get(
            "https://www.googleapis.com/youtube/v3/videos", json=mock_response
        )
        with pytest.raises(ValueError, match="Video not found"):
            get_video_metadata("nonexistent", "fake_api_key")

    def test_api_error(self, requests_mock):
        requests_mock.get(
            "https://www.googleapis.com/youtube/v3/videos", status_code=403
        )
        with pytest.raises(Exception):
            get_video_metadata("test123", "fake_api_key")


class TestGetTranscript:
    def test_fetch_transcript_success(self, mocker):
        mock_transcript_list = [
            {"text": "Hello", "start": 0.0, "duration": 1.0},
            {"text": "World", "start": 1.0, "duration": 1.0},
        ]
        mock_api = mocker.patch("get_youtube_data.YouTubeTranscriptApi")
        mock_api.return_value.fetch.return_value = mock_transcript_list

        result = get_transcript("test123")
        assert result == "Hello World"

    def test_transcript_not_available(self, mocker):
        mock_api = mocker.patch("get_youtube_data.YouTubeTranscriptApi")
        mock_api.return_value.fetch.side_effect = Exception("No transcript available")

        with pytest.raises(ValueError, match="Could not fetch transcript"):
            get_transcript("nonexistent")


class TestIntegration:
    @pytest.mark.skipif(
        not os.environ.get("YOUTUBE_API_KEY"),
        reason="YOUTUBE_API_KEY not set",
    )
    def test_real_youtube_api(self):
        api_key = os.environ.get("YOUTUBE_API_KEY")
        video_id = "dQw4w9WgXcQ"

        metadata = get_video_metadata(video_id, api_key)
        assert metadata["title"]
        assert isinstance(metadata["description"], str)
        assert isinstance(metadata["tags"], list)

#!/usr/bin/env python3
import os
import sys

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "skills",
        "youtube-obsidian",
        "scripts",
    ),
)

import pytest
from get_youtube_data import (
    create_obsidian_note,
    extract_video_id,
    generate_tags,
    get_transcript,
    get_video_metadata,
    sanitize_filename,
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


class MockTranscriptEntry:
    def __init__(self, text, start, duration):
        self.text = text
        self.start = start
        self.duration = duration


class TestGetTranscript:
    def test_fetch_transcript_success(self, mocker):
        mock_transcript_list = [
            MockTranscriptEntry("Hello", 0.0, 1.0),
            MockTranscriptEntry("World", 1.0, 1.0),
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


class TestMainFunction:
    def test_main_no_arguments(self, capsys, mocker):
        mocker.patch("sys.argv", ["get_youtube_data.py"])
        with pytest.raises(SystemExit) as exc_info:
            import get_youtube_data

            get_youtube_data.main()
        assert exc_info.value.code == 1

    def test_main_missing_api_key(self, capsys, mocker, monkeypatch):
        mocker.patch(
            "sys.argv", ["get_youtube_data.py", "https://youtube.com/watch?v=test"]
        )
        monkeypatch.delenv("YOUTUBE_API_KEY", raising=False)
        monkeypatch.setenv("VAULT_PATH", "/tmp")
        with pytest.raises(SystemExit) as exc_info:
            import get_youtube_data

            get_youtube_data.main()
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "YOUTUBE_API_KEY environment variable not set" in captured.out

    def test_main_missing_vault_path(self, capsys, mocker, monkeypatch):
        mocker.patch(
            "sys.argv", ["get_youtube_data.py", "https://youtube.com/watch?v=test"]
        )
        monkeypatch.setenv("YOUTUBE_API_KEY", "fake_key")
        monkeypatch.delenv("VAULT_PATH", raising=False)
        monkeypatch.delenv("OBSIDIAN_VAULT_PATH", raising=False)
        with pytest.raises(SystemExit) as exc_info:
            import get_youtube_data

            get_youtube_data.main()
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert (
            "VAULT_PATH or OBSIDIAN_VAULT_PATH environment variable not set"
            in captured.out
        )

    def test_main_success_flow(self, mocker, monkeypatch, tmp_path):
        mocker.patch(
            "sys.argv", ["get_youtube_data.py", "https://youtube.com/watch?v=test123"]
        )
        monkeypatch.setenv("YOUTUBE_API_KEY", "fake_key")
        monkeypatch.setenv("VAULT_PATH", str(tmp_path))

        mocker.patch("get_youtube_data.extract_video_id", return_value="test123")
        mocker.patch(
            "get_youtube_data.get_video_metadata",
            return_value={"title": "Test", "description": "Desc", "tags": []},
        )
        mocker.patch("get_youtube_data.get_transcript", return_value="Transcript text")
        mocker.patch(
            "get_youtube_data.create_obsidian_note",
            return_value=("Note content", "test_note"),
        )

        import get_youtube_data

        get_youtube_data.main()

        assert (tmp_path / "test_note.md").exists()

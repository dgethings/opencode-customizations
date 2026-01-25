import json
import os
from unittest.mock import patch

import pytest
import write_obsidian_note
from pydantic import AnyUrl
from typer import Exit
from typer.testing import CliRunner

runner = CliRunner()


class TestSanitizeFilename:
    def test_sanitize_filename_basic(self):
        result = write_obsidian_note.sanitize_filename("Test Video Title")
        assert result == "Test Video Title"

    def test_sanitize_filename_with_invalid_chars(self):
        result = write_obsidian_note.sanitize_filename("Test:Video<>Title")
        assert result == "TestVideoTitle"

    def test_sanitize_filename_with_slashes(self):
        result = write_obsidian_note.sanitize_filename("Test/Video\\Title")
        assert result == "TestVideoTitle"

    def test_sanitize_filename_with_quotes(self):
        result = write_obsidian_note.sanitize_filename('Test"Video"Title')
        assert result == "TestVideoTitle"

    def test_sanitize_filename_with_pipe(self):
        result = write_obsidian_note.sanitize_filename("Test|Video")
        assert result == "TestVideo"

    def test_sanitize_filename_with_question_mark(self):
        result = write_obsidian_note.sanitize_filename("Test?Video")
        assert result == "TestVideo"

    def test_sanitize_filename_with_asterisk(self):
        result = write_obsidian_note.sanitize_filename("Test*Video")
        assert result == "TestVideo"

    def test_sanitize_filename_with_leading_trailing_spaces(self):
        result = write_obsidian_note.sanitize_filename("  Test Video  ")
        assert result == "Test Video"

    def test_sanitize_filename_with_trailing_period(self):
        result = write_obsidian_note.sanitize_filename("Test Video.")
        assert result == "Test Video"

    def test_sanitize_filename_too_long(self):
        long_title = "A" * 150
        result = write_obsidian_note.sanitize_filename(long_title)
        assert len(result) == 100
        assert result.endswith("...")

    def test_sanitize_filename_empty_after_sanitization(self):
        result = write_obsidian_note.sanitize_filename("???...")
        assert result == "video"


class TestGenerateTags:
    def test_generate_tags_from_title(self):
        result = write_obsidian_note.generate_tags("Python Tutorial", "", "")
        assert "python" in result
        assert "tutorial" in result

    def test_generate_tags_from_description(self):
        result = write_obsidian_note.generate_tags("", "Learn Machine Learning", "")
        assert "machine learning" in result

    def test_generate_tags_from_transcript(self):
        result = write_obsidian_note.generate_tags(
            "", "", "This is about Docker and Kubernetes"
        )
        assert "docker" in result
        assert "kubernetes" in result

    def test_generate_tags_with_youtube_tags(self):
        result = write_obsidian_note.generate_tags(
            "Python", "Tutorial", "", youtube_tags=["python", "programming"]
        )
        assert "python" in result
        assert "programming" in result

    def test_generate_tags_capitalized_keywords(self):
        result = write_obsidian_note.generate_tags(
            "Machine Learning in Python", "This is a Python Tutorial", ""
        )
        assert "machine learning" in result or "learning" in result

    def test_generate_tags_short_keywords_filtered(self):
        result = write_obsidian_note.generate_tags("AI and ML Tutorial", "", "")
        assert "ml" not in result

    def test_generate_tags_max_five_tags(self):
        result = write_obsidian_note.generate_tags(
            "Python and JavaScript Tutorial",
            "Learn Docker and Kubernetes",
            "This is about Machine Learning and AI",
        )
        assert len(result) <= 5

    def test_generate_tags_no_matching_terms(self):
        result = write_obsidian_note.generate_tags(
            "Random Title", "Random description", ""
        )
        assert len(result) <= 5

    def test_generate_tags_empty_inputs(self):
        result = write_obsidian_note.generate_tags("", "", "")
        assert isinstance(result, list)


class TestMetadata:
    def test_metadata_valid_json_file(self, tmp_path):
        test_data = {
            "id": "test_id",
            "title": "Test Title",
            "description": "Test Description",
            "tags": ["python", "tutorial"],
            "user_comments": "",
            "summary": "Test Summary",
            "url": "https://www.youtube.com/watch?v=test_id",
            "transcript": "Test Transcript",
        }
        json_file = tmp_path / "test_data.json"
        json_file.write_text(json.dumps(test_data))

        result = write_obsidian_note.metadata(str(json_file))
        assert result.id == "test_id"
        assert result.title == "Test Title"
        assert result.description == "Test Description"

    def test_metadata_invalid_json(self, tmp_path, capsys):
        json_file = tmp_path / "invalid.json"
        json_file.write_text("not valid json")

        with pytest.raises(Exit):
            write_obsidian_note.metadata(str(json_file))

        captured = capsys.readouterr()
        assert captured.out

    def test_metadata_missing_fields(self, tmp_path):
        incomplete_data = {"id": "test_id"}
        json_file = tmp_path / "incomplete.json"
        json_file.write_text(json.dumps(incomplete_data))

        with pytest.raises(Exit):
            write_obsidian_note.metadata(str(json_file))


class TestWriteNote:
    @patch.dict(os.environ, {"VAULT_PATH": "/test/vault"})
    @patch("write_obsidian_note.Path.write_text")
    def test_write_note_success(self, mock_write):
        write_obsidian_note.write_note("test.md", "Test content")
        mock_write.assert_called_once_with("Test content")

    @patch.dict(os.environ, {}, clear=True)
    @patch("write_obsidian_note.Path.write_text")
    def test_write_note_missing_vault_path(self, mock_write, capsys):
        with pytest.raises(Exit):
            write_obsidian_note.write_note("test.md", "Test content")

        captured = capsys.readouterr()
        assert "VAULT_PATH not set" in captured.out


class TestYtTemplate:
    def test_yt_template_basic(self):
        test_data = write_obsidian_note.Data(
            id="test_id",
            title="Test Title",
            description="Test Description",
            tags=["python", "tutorial"],
            user_comments="",
            summary="Test Summary",
            url=AnyUrl("https://www.youtube.com/watch?v=test_id"),
            transcript="Test Transcript",
        )
        result = write_obsidian_note.yt_template(test_data)

        assert "---" in result
        assert "title: Test Title" in result
        assert "youtube_id: test_id" in result
        assert "tags:" in result
        assert "youtube_url: https://www.youtube.com/watch?v=test_id" in result
        assert "created:" in result
        assert "# Test Title" in result
        assert "## Description" in result
        assert "Test Description" in result
        assert "## Transcript" in result
        assert "Test Transcript" in result

    def test_yt_template_with_comments(self):
        test_data = write_obsidian_note.Data(
            id="test_id",
            title="Test Title",
            description="Test Description",
            tags=["python"],
            user_comments="Great video!",
            summary="Test Summary",
            url=AnyUrl("https://www.youtube.com/watch?v=test_id"),
            transcript="Test Transcript",
        )
        result = write_obsidian_note.yt_template(test_data)

        assert "## Comments" in result
        assert "Great video!" in result

    def test_yt_template_without_comments(self):
        test_data = write_obsidian_note.Data(
            id="test_id",
            title="Test Title",
            description="Test Description",
            tags=["python"],
            user_comments="",
            summary="Test Summary",
            url=AnyUrl("https://www.youtube.com/watch?v=test_id"),
            transcript="Test Transcript",
        )
        result = write_obsidian_note.yt_template(test_data)

        assert "## Comments" not in result

    def test_yt_template_tags_format(self):
        test_data = write_obsidian_note.Data(
            id="test_id",
            title="Test Title",
            description="Test Description",
            tags=["python", "javascript", "tutorial"],
            user_comments="",
            summary="Test Summary",
            url=AnyUrl("https://www.youtube.com/watch?v=test_id"),
            transcript="Test Transcript",
        )
        result = write_obsidian_note.yt_template(test_data)

        assert json.dumps(["python", "javascript", "tutorial"]) in result


class TestCreateObsidianNoteCommand:
    @patch("write_obsidian_note.metadata")
    def test_create_obsidian_note_invalid_json(self, mock_metadata, tmp_path, capsys):
        mock_metadata.side_effect = Exit(1)

        json_file = tmp_path / "invalid.json"
        json_file.write_text("invalid json")

        result = runner.invoke(
            write_obsidian_note.app, ["create-obsidian-note", str(json_file)]
        )

        assert result.exit_code == 1

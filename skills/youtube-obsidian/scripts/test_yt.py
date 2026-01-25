import json
import os
from collections import namedtuple
from unittest.mock import MagicMock, patch

import pytest
import requests
import yt
from pydantic_core import ValidationError
from typer import Exit
from typer.testing import CliRunner
from youtube_transcript_api import VideoUnavailable

runner = CliRunner()

TranscriptItem = namedtuple("TranscriptItem", ["text", "start", "duration"])


class TestFetchTranscript:
    @patch("yt.YouTubeTranscriptApi")
    def test_fetch_transcript_success(self, mock_api_class):
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_api.fetch.return_value = [
            TranscriptItem(text="Hello ", start=0.0, duration=0.5),
            TranscriptItem(text="world", start=0.5, duration=0.5),
        ]

        result = yt.fetch_transcript("test_video_id")
        assert result == "Hello  world "

    @patch("yt.YouTubeTranscriptApi")
    def test_fetch_transcript_with_custom_langs(self, mock_api_class):
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_api.fetch.return_value = [
            TranscriptItem(text="Test", start=0.0, duration=1.0)
        ]

        result = yt.fetch_transcript("test_video_id", langs=["es", "en"])
        assert result == "Test "
        mock_api.fetch.assert_called_once_with("test_video_id", ["es", "en"])

    @patch("yt.YouTubeTranscriptApi")
    @patch("yt.echo")
    def test_fetch_transcript_video_unavailable(self, mock_echo, mock_api_class):
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_api.fetch.side_effect = VideoUnavailable("Video not found")

        try:
            yt.fetch_transcript("unavailable_video")
            assert False, "Should have raised Exit"
        except Exit as e:
            assert e.exit_code == 1

    @patch("yt.YouTubeTranscriptApi")
    @patch("yt.echo")
    def test_fetch_transcript_generic_error(self, mock_echo, mock_api_class):
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_api.fetch.side_effect = Exception("Network error")

        try:
            yt.fetch_transcript("test_video_id")
            assert False, "Should have raised Exit"
        except Exit as e:
            assert e.exit_code == 2

    @patch("yt.YouTubeTranscriptApi")
    def test_fetch_transcript_empty_result(self, mock_api_class):
        mock_api = MagicMock()
        mock_api_class.return_value = mock_api
        mock_api.fetch.return_value = []

        result = yt.fetch_transcript("test_video_id")
        assert result == ""


class TestTranscriptCommand:
    @patch("yt.fetch_transcript")
    def test_transcript_command_default_lang(self, mock_fetch):
        mock_fetch.return_value = "Test transcript "
        result = runner.invoke(yt.app, ["transcript", "test_video_id"])
        assert result.exit_code == 0
        mock_fetch.assert_called_once_with("test_video_id", ["en"])

    @patch("yt.fetch_transcript")
    def test_transcript_command_with_lang_option(self, mock_fetch):
        mock_fetch.return_value = "Test transcript "
        result = runner.invoke(yt.app, ["transcript", "test_video_id", "--lang", "es"])
        assert result.exit_code == 0
        mock_fetch.assert_called_once_with("test_video_id", ["es"])


class TestParseYtUrl:
    def test_parse_yt_url_valid(self):
        result = yt.parse_yt_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        assert str(result) == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    def test_parse_yt_url_short(self):
        result = yt.parse_yt_url("https://youtu.be/dQw4w9WgXcQ")
        assert str(result) == "https://youtu.be/dQw4w9WgXcQ"

    def test_parse_yt_url_invalid(self):
        with pytest.raises(ValidationError):
            yt.parse_yt_url("not a valid url")

    def test_parse_yt_url_empty_string(self):
        with pytest.raises(ValidationError):
            yt.parse_yt_url("")


class TestIdCommand:
    def test_id_command_valid_url(self):
        result = runner.invoke(
            yt.app, ["id", "https://www.youtube.com/watch?v=dQw4w9WgXcQ"]
        )
        assert result.exit_code == 0
        assert "dQw4w9WgXcQ" in result.stdout

    def test_id_command_url_missing_v_param(self):
        result = runner.invoke(yt.app, ["id", "https://www.youtube.com/watch"])
        assert result.exit_code == 3
        assert "missing the 'v' parameter" in result.stdout

    def test_id_command_short_url(self):
        result = runner.invoke(yt.app, ["id", "https://youtu.be/dQw4w9WgXcQ"])
        assert result.exit_code == 3
        assert "missing the 'v' parameter" in result.stdout


class TestYtDataApi:
    @patch("yt.requests.get")
    def test_yt_data_api_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {"snippet": {"title": "Test Video", "description": "Test Description"}}
            ]
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        result = yt.yt_data_api("test_video_id", api_key="test_api_key")
        assert result.title == "Test Video"
        assert result.description == "Test Description"

    @patch.dict(os.environ, {}, clear=True)
    @patch("yt.echo")
    def test_yt_data_api_missing_api_key(self, mock_echo):
        try:
            yt.yt_data_api("test_video_id", api_key=None)
            assert False, "Should have raised Exit"
        except Exit as e:
            assert e.exit_code == 4

    @patch("yt.requests.get")
    def test_yt_data_api_custom_url(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {"snippet": {"title": "Test Video", "description": "Test Description"}}
            ]
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        result = yt.yt_data_api(
            "test_video_id", api_key="test_api_key", url="https://mock-api.com/videos"
        )
        assert result.title == "Test Video"
        mock_get.assert_called_once()

    @patch("yt.requests.get")
    def test_yt_data_api_http_error(self, mock_get):
        mock_get.side_effect = requests.HTTPError("404 Not Found")

        with pytest.raises(requests.HTTPError):
            yt.yt_data_api("test_video_id", api_key="test_api_key")

    @patch("yt.requests.get")
    def test_yt_data_api_video_not_found(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": []}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        with pytest.raises(ValueError, match="Video not found"):
            yt.yt_data_api("test_video_id", api_key="test_api_key")

    @patch("yt.requests.get")
    @patch("yt.echo")
    def test_yt_data_api_missing_snippet(self, mock_echo, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": [{"id": "test"}]}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        try:
            yt.yt_data_api("test_video_id", api_key="test_api_key")
            assert False, "Should have raised Exit"
        except Exit as e:
            assert e.exit_code == 5


class TestGetMetadata:
    @patch("yt.yt_data_api")
    def test_get_metadata_success(self, mock_yt_data_api):
        mock_yt_data_api.return_value = yt.Snippet(
            title="Test Video", description="Test Description"
        )

        result = yt.get_metadata("test_video_id")
        metadata = json.loads(result)
        assert metadata["title"] == "Test Video"
        assert metadata["description"] == "Test Description"


class TestMetadataCommand:
    @patch("yt.yt_data_api")
    def test_metadata_command_success(self, mock_yt_data_api):
        mock_yt_data_api.return_value = yt.Snippet(
            title="Test Video", description="Test Description"
        )

        result = runner.invoke(yt.app, ["metadata", "test_video_id"])
        assert result.exit_code == 0
        output_data = json.loads(result.stdout)
        assert output_data["title"] == "Test Video"
        assert output_data["description"] == "Test Description"

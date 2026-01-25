from collections import namedtuple
from unittest.mock import MagicMock, patch

import yt
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
        result = runner.invoke(yt.app, ["test_video_id"])
        assert result.exit_code == 0
        mock_fetch.assert_called_once_with("test_video_id", ["en"])

    @patch("yt.fetch_transcript")
    def test_transcript_command_with_lang_option(self, mock_fetch):
        mock_fetch.return_value = "Test transcript "
        result = runner.invoke(yt.app, ["test_video_id", "--lang", "es"])
        assert result.exit_code == 0
        mock_fetch.assert_called_once_with("test_video_id", ["es"])

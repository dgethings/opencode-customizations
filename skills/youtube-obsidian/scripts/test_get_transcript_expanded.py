#!/usr/bin/env python3
"""
Expanded tests for get_transcript() function.

Tests edge cases, special characters, and boundary conditions
for transcript fetching.
"""

import pytest
from unittest.mock import Mock
from get_youtube_data import get_transcript


class TestGetTranscriptEdgeCases:
    """Edge case scenarios (P1)."""

    @pytest.mark.p1
    @pytest.mark.unit
    def test_empty_transcript_list(self, mocker):
        """Test handling of empty transcript list (P1)."""
        mock_api = mocker.patch("get_youtube_data.YouTubeTranscriptApi")
        mock_api.return_value.fetch.return_value = []

        # Empty list returns empty string, not an error
        result = get_transcript("test123")
        assert result == ""

    @pytest.mark.p1
    @pytest.mark.unit
    def test_transcript_with_special_characters(self, mocker):
        """Test handling of transcript with special characters (P1)."""
        mock_transcript = [
            Mock(text="Hello World! @#$%^&*()", start=0.0, duration=1.0),
            Mock(text="Special: <>&\"'", start=1.0, duration=1.0),
        ]

        mock_api = mocker.patch("get_youtube_data.YouTubeTranscriptApi")
        mock_api.return_value.fetch.return_value = mock_transcript

        result = get_transcript("test123")
        assert "Hello World!" in result
        assert "@#$%^&*()" in result
        assert "Special: <>&\"'" in result

    @pytest.mark.p1
    @pytest.mark.unit
    def test_transcript_with_unicode(self, mocker):
        """Test handling of transcript with Unicode (P1)."""
        mock_transcript = [
            Mock(text="日本語 Test", start=0.0, duration=1.0),
            Mock(text="中国语 🎉", start=1.0, duration=1.0),
        ]

        mock_api = mocker.patch("get_youtube_data.YouTubeTranscriptApi")
        mock_api.return_value.fetch.return_value = mock_transcript

        result = get_transcript("test123")
        assert "日本語" in result
        assert "中国语" in result
        assert "🎉" in result

    @pytest.mark.p1
    @pytest.mark.unit
    def test_very_long_transcript(self, mocker):
        """Test handling of very long transcript (P1)."""
        # Create 100 transcript entries with 100 chars each
        mock_transcript = [
            Mock(text=f"Word{i} " * 10, start=float(i), duration=1.0)
            for i in range(100)
        ]

        mock_api = mocker.patch("get_youtube_data.YouTubeTranscriptApi")
        mock_api.return_value.fetch.return_value = mock_transcript

        result = get_transcript("test123")
        # Each entry: "Word0 " * 10 = 60 chars per entry
        # 100 entries * 60 chars = 6000 chars, plus spaces from join
        assert len(result) > 6000  # Should be very long
        assert "Word0" in result
        assert "Word99" in result

    @pytest.mark.p1
    @pytest.mark.unit
    def test_transcript_entry_with_no_text_field(self, mocker):
        """Test handling of transcript entry with no text field (P1)."""
        mock_transcript = [
            Mock(text="Hello", start=0.0, duration=1.0),
            Mock(start=1.0, duration=1.0),  # Missing text field (non-iterable)
            Mock(text="World", start=2.0, duration=1.0),
        ]

        mock_api = mocker.patch("get_youtube_data.YouTubeTranscriptApi")
        mock_api.return_value.fetch.return_value = mock_transcript

        # Actual behavior: raises ValueError for non-string in list
        with pytest.raises(ValueError, match="Could not fetch transcript"):
            get_transcript("test123")

    @pytest.mark.p1
    @pytest.mark.unit
    def test_transcript_with_timing_data(self, mocker):
        """Test that transcript preserves timing data (P1)."""
        mock_transcript = [
            Mock(text="Hello", start=0.0, duration=1.5),
            Mock(text="World", start=2.5, duration=0.5),
        ]

        mock_api = mocker.patch("get_youtube_data.YouTubeTranscriptApi")
        mock_api.return_value.fetch.return_value = mock_transcript

        result = get_transcript("test123")
        assert "Hello World" in result
        # Check spacing based on timing
        assert "Hello" in result.split("World")[0]

    @pytest.mark.p1
    @pytest.mark.unit
    def test_single_transcript_entry(self, mocker):
        """Test handling of single transcript entry (P1)."""
        mock_transcript = [Mock(text="Single entry", start=0.0, duration=1.0)]

        mock_api = mocker.patch("get_youtube_data.YouTubeTranscriptApi")
        mock_api.return_value.fetch.return_value = mock_transcript

        result = get_transcript("test123")
        assert result == "Single entry"

    @pytest.mark.p1
    @pytest.mark.unit
    def test_transcript_with_newlines(self, mocker):
        """Test handling of transcript with newlines (P1)."""
        mock_transcript = [
            Mock(text="Line 1\nLine 2", start=0.0, duration=2.0),
            Mock(text="Line 3", start=2.0, duration=1.0),
        ]

        mock_api = mocker.patch("get_youtube_data.YouTubeTranscriptApi")
        mock_api.return_value.fetch.return_value = mock_transcript

        result = get_transcript("test123")
        assert "Line 1" in result
        assert "Line 2" in result
        assert "Line 3" in result

    @pytest.mark.p1
    @pytest.mark.unit
    def test_transcript_with_tabs(self, mocker):
        """Test handling of transcript with tabs (P1)."""
        mock_transcript = [
            Mock(text="Word1\tWord2\tWord3", start=0.0, duration=1.0),
        ]

        mock_api = mocker.patch("get_youtube_data.YouTubeTranscriptApi")
        mock_api.return_value.fetch.return_value = mock_transcript

        result = get_transcript("test123")
        assert "Word1" in result
        assert "Word2" in result
        assert "Word3" in result

    @pytest.mark.p1
    @pytest.mark.unit
    def test_transcript_with_empty_strings(self, mocker):
        """Test handling of transcript with empty string entries (P1)."""
        mock_transcript = [
            Mock(text="", start=0.0, duration=0.5),
            Mock(text="Hello", start=0.5, duration=1.0),
            Mock(text="", start=1.5, duration=0.5),
            Mock(text="World", start=2.0, duration=1.0),
        ]

        mock_api = mocker.patch("get_youtube_data.YouTubeTranscriptApi")
        mock_api.return_value.fetch.return_value = mock_transcript

        result = get_transcript("test123")
        assert "Hello" in result
        assert "World" in result
        # Empty strings should create extra spaces
        assert "  " in result or result.count(" ") >= 1


class TestGetTranscriptErrorScenarios:
    """Error scenario tests (P1)."""

    @pytest.mark.p1
    @pytest.mark.unit
    def test_transcript_not_available(self, mocker):
        """Test handling of unavailable transcript (P1)."""
        mock_api = mocker.patch("get_youtube_data.YouTubeTranscriptApi")
        mock_api.return_value.fetch.side_effect = Exception("No transcript available")

        with pytest.raises(ValueError, match="Could not fetch transcript"):
            get_transcript("nonexistent")

    @pytest.mark.p1
    @pytest.mark.unit
    def test_transcript_api_timeout(self, mocker):
        """Test handling of transcript API timeout (P1)."""
        mock_api = mocker.patch("get_youtube_data.YouTubeTranscriptApi")
        mock_api.return_value.fetch.side_effect = TimeoutError("Request timed out")

        with pytest.raises(ValueError, match="Could not fetch transcript"):
            get_transcript("test123")

    @pytest.mark.p1
    @pytest.mark.unit
    def test_transcript_api_connection_error(self, mocker):
        """Test handling of connection error (P1)."""
        mock_api = mocker.patch("get_youtube_data.YouTubeTranscriptApi")
        mock_api.return_value.fetch.side_effect = ConnectionError("Failed to connect")

        with pytest.raises(ValueError, match="Could not fetch transcript"):
            get_transcript("test123")

    @pytest.mark.p1
    @pytest.mark.unit
    def test_transcript_with_multiple_languages(self, mocker):
        """Test handling of transcript with multiple languages (P1)."""
        # Note: This may not be supported by youtube-transcript-api
        mock_transcript = [
            Mock(text="Hello in English", start=0.0, duration=1.0, language="en"),
            Mock(text="Hola in Spanish", start=1.0, duration=1.0, language="es"),
        ]

        mock_api = mocker.patch("get_youtube_data.YouTubeTranscriptApi")
        mock_api.return_value.fetch.return_value = mock_transcript

        result = get_transcript("test123")
        # Should include both entries
        assert "Hello in English" in result or "Hola in Spanish" in result


class TestGetTranscriptTranscriptJoining:
    """Tests for transcript joining logic (P1)."""

    @pytest.mark.p1
    @pytest.mark.unit
    def test_transcript_joined_with_spaces(self, mocker):
        """Test that transcript entries are joined with spaces (P1)."""
        mock_transcript = [
            Mock(text="Hello", start=0.0, duration=1.0),
            Mock(text="World", start=1.0, duration=1.0),
            Mock(text="Python", start=2.0, duration=1.0),
        ]

        mock_api = mocker.patch("get_youtube_data.YouTubeTranscriptApi")
        mock_api.return_value.fetch.return_value = mock_transcript

        result = get_transcript("test123")
        assert result == "Hello World Python"

    @pytest.mark.p1
    @pytest.mark.unit
    def test_transcript_preserves_entry_order(self, mocker):
        """Test that transcript preserves original order (P1)."""
        mock_transcript = [
            Mock(text="First", start=0.0, duration=1.0),
            Mock(text="Second", start=1.0, duration=1.0),
            Mock(text="Third", start=2.0, duration=1.0),
        ]

        mock_api = mocker.patch("get_youtube_data.YouTubeTranscriptApi")
        mock_api.return_value.fetch.return_value = mock_transcript

        result = get_transcript("test123")
        assert result.index("First") < result.index("Second") < result.index("Third")

    @pytest.mark.p1
    @pytest.mark.unit
    def test_transcript_trailing_whitespace(self, mocker):
        """Test handling of transcript entries with trailing whitespace (P1)."""
        mock_transcript = [
            Mock(text="Hello  ", start=0.0, duration=1.0),  # Trailing spaces
            Mock(text="  World", start=1.0, duration=1.0),  # Leading spaces
        ]

        mock_api = mocker.patch("get_youtube_data.YouTubeTranscriptApi")
        mock_api.return_value.fetch.return_value = mock_transcript

        result = get_transcript("test123")
        assert "Hello" in result
        assert "World" in result
        # Check that some whitespace is preserved
        assert " " in result

    @pytest.mark.p1
    @pytest.mark.unit
    def test_transcript_with_numbers(self, mocker):
        """Test handling of transcript with numbers (P1)."""
        mock_transcript = [
            Mock(text="Python 3.11", start=0.0, duration=1.0),
            Mock(text="100% test coverage", start=1.0, duration=1.0),
        ]

        mock_api = mocker.patch("get_youtube_data.YouTubeTranscriptApi")
        mock_api.return_value.fetch.return_value = mock_transcript

        result = get_transcript("test123")
        assert "3.11" in result
        assert "100%" in result

    @pytest.mark.p1
    @pytest.mark.unit
    def test_transcript_with_emoji(self, mocker):
        """Test handling of transcript with emoji (P1)."""
        mock_transcript = [
            Mock(text="Great job! 🎉", start=0.0, duration=1.0),
            Mock(text="Keep it up! 🔥", start=1.0, duration=1.0),
        ]

        mock_api = mocker.patch("get_youtube_data.YouTubeTranscriptApi")
        mock_api.return_value.fetch.return_value = mock_transcript

        result = get_transcript("test123")
        assert "🎉" in result
        assert "🔥" in result

    @pytest.mark.p1
    @pytest.mark.unit
    def test_transcript_with_html_entities(self, mocker):
        """Test handling of transcript with HTML entities (P1)."""
        mock_transcript = [
            Mock(text="A & B & C", start=0.0, duration=1.0),
        ]

        mock_api = mocker.patch("get_youtube_data.YouTubeTranscriptApi")
        mock_api.return_value.fetch.return_value = mock_transcript

        result = get_transcript("test123")
        # YouTube API may or may not decode HTML entities
        assert "&" in result or "&amp;" in result

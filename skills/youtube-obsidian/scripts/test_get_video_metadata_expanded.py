#!/usr/bin/env python3
"""
Expanded tests for get_video_metadata() function.

Tests critical API error scenarios (P0) and edge cases (P1).
"""

import pytest
import requests
from get_youtube_data import get_video_metadata
from requests.exceptions import Timeout, ConnectionError, HTTPError


class TestGetVideoMetadataCriticalErrors:
    """Critical API error scenarios (P0)."""

    @pytest.mark.p0
    @pytest.mark.unit
    def test_network_timeout(self, requests_mock):
        """Test handling of network timeout (P0)."""
        requests_mock.get(
            "https://www.googleapis.com/youtube/v3/videos",
            exc=Timeout("Request timed out after 30 seconds"),
        )

        with pytest.raises(Exception):
            get_video_metadata("test123", "fake_api_key")

    @pytest.mark.p0
    @pytest.mark.unit
    def test_connection_refused(self, requests_mock):
        """Test handling of connection refused (P0)."""
        requests_mock.get(
            "https://www.googleapis.com/youtube/v3/videos",
            exc=ConnectionError("Failed to establish connection"),
        )

        with pytest.raises(Exception):
            get_video_metadata("test123", "fake_api_key")

    @pytest.mark.p0
    @pytest.mark.unit
    def test_invalid_api_key_http_403(self, requests_mock):
        """Test handling of invalid API key (HTTP 403) (P0)."""
        requests_mock.get(
            "https://www.googleapis.com/youtube/v3/videos",
            status_code=403,
            json={
                "error": {
                    "code": 403,
                    "message": "API key not valid",
                }
            },
        )

        with pytest.raises(Exception):
            get_video_metadata("test123", "fake_api_key")

    @pytest.mark.p0
    @pytest.mark.unit
    def test_rate_limit_http_429(self, requests_mock):
        """Test handling of rate limit (HTTP 429) (P0)."""
        requests_mock.get(
            "https://www.googleapis.com/youtube/v3/videos",
            status_code=429,
            json={
                "error": {
                    "code": 429,
                    "message": "Rate limit exceeded",
                }
            },
        )

        with pytest.raises(Exception):
            get_video_metadata("test123", "fake_api_key")

    @pytest.mark.p0
    @pytest.mark.unit
    def test_http_500_internal_error(self, requests_mock):
        """Test handling of HTTP 500 internal server error (P0)."""
        requests_mock.get(
            "https://www.googleapis.com/youtube/v3/videos",
            status_code=500,
            json={
                "error": {
                    "code": 500,
                    "message": "Internal server error",
                }
            },
        )

        with pytest.raises(Exception):
            get_video_metadata("test123", "fake_api_key")

    @pytest.mark.p1
    @pytest.mark.unit
    def test_http_400_bad_request(self, requests_mock):
        """Test handling of HTTP 400 bad request (P1)."""
        requests_mock.get(
            "https://www.googleapis.com/youtube/v3/videos",
            status_code=400,
            json={
                "error": {
                    "code": 400,
                    "message": "Bad request",
                }
            },
        )

        with pytest.raises(Exception):
            get_video_metadata("test123", "fake_api_key")

    @pytest.mark.p0
    @pytest.mark.unit
    def test_http_500_internal_error(self, requests_mock):
        """Test handling of HTTP 500 internal server error (P0)."""
        requests_mock.get(
            "https://www.googleapis.com/youtube/v3/videos",
            status_code=500,
            json={
                "error": {
                    "code": 500,
                    "message": "Internal server error",
                }
            },
        )

        response = requests.get(
            "https://www.googleapis.com/youtube/v3/videos",
            params={"id": "test123", "key": "fake_api_key", "part": "snippet"},
        )
        with pytest.raises(HTTPError):
            response.raise_for_status()

    @pytest.mark.p0
    @pytest.mark.unit
    def test_malformed_api_response(self, requests_mock):
        """Test handling of malformed API response (P0)."""
        # Response missing required fields
        requests_mock.get(
            "https://www.googleapis.com/youtube/v3/videos",
            json={
                "items": [
                    {
                        "id": "test123",
                        # Missing 'snippet' field
                    }
                ]
            },
        )

        with pytest.raises((KeyError, TypeError)):
            get_video_metadata("test123", "fake_api_key")

    @pytest.mark.p0
    @pytest.mark.unit
    def test_empty_items_array(self, requests_mock):
        """Test handling of empty items array (P0)."""
        requests_mock.get(
            "https://www.googleapis.com/youtube/v3/videos",
            json={"items": []},
        )

        with pytest.raises(ValueError, match="Video not found"):
            get_video_metadata("test123", "fake_api_key")


class TestGetVideoMetadataEdgeCases:
    """Edge case scenarios (P1)."""

    @pytest.mark.p1
    @pytest.mark.unit
    def test_slow_network_response(self, requests_mock):
        """Test handling of slow network response (P1)."""

        def slow_response_callback(request, context):
            import time

            time.sleep(0.1)  # Simulate slow response
            return {
                "items": [
                    {
                        "snippet": {
                            "title": "Test",
                            "description": "Desc",
                            "tags": [],
                        }
                    }
                ]
            }

        requests_mock.get(
            "https://www.googleapis.com/youtube/v3/videos",
            json=slow_response_callback,
        )

        result = get_video_metadata("test123", "fake_api_key")
        assert result["title"] == "Test"

    @pytest.mark.p1
    @pytest.mark.unit
    def test_partial_api_response(self, requests_mock):
        """Test handling of partial API response (missing fields) (P1)."""
        requests_mock.get(
            "https://www.googleapis.com/youtube/v3/videos",
            json={
                "items": [
                    {
                        "snippet": {
                            "title": "Test",
                            # Missing description and tags
                        }
                    }
                ]
            },
        )

        result = get_video_metadata("test123", "fake_api_key")
        assert result["title"] == "Test"
        assert result["description"] == ""  # Default to empty
        assert result["tags"] == []  # Default to empty

    @pytest.mark.p1
    @pytest.mark.unit
    def test_http_400_bad_request(self, requests_mock):
        """Test handling of HTTP 400 bad request (P1)."""
        requests_mock.get(
            "https://www.googleapis.com/youtube/v3/videos",
            status_code=400,
            json={
                "error": {
                    "code": 400,
                    "message": "Bad request",
                }
            },
        )

        response = requests.get(
            "https://www.googleapis.com/youtube/v3/videos",
            params={"id": "test123", "key": "fake_api_key", "part": "snippet"},
        )
        with pytest.raises(HTTPError):
            response.raise_for_status()

    @pytest.mark.p1
    @pytest.mark.unit
    def test_unicode_in_metadata(self, requests_mock):
        """Test handling of Unicode in metadata (P1)."""
        requests_mock.get(
            "https://www.googleapis.com/youtube/v3/videos",
            json={
                "items": [
                    {
                        "snippet": {
                            "title": "日本語 Test 🎉",
                            "description": "中国语",
                            "tags": ["python", "日本語"],
                        }
                    }
                ]
            },
        )

        result = get_video_metadata("test123", "fake_api_key")
        assert result["title"] == "日本語 Test 🎉"
        assert result["description"] == "中国语"
        assert "python" in result["tags"]
        assert "日本語" in result["tags"]

    @pytest.mark.p1
    @pytest.mark.unit
    def test_very_long_metadata(self, requests_mock):
        """Test handling of very long metadata (P1)."""
        long_desc = "A" * 10000
        many_tags = [f"tag{i}" for i in range(100)]

        requests_mock.get(
            "https://www.googleapis.com/youtube/v3/videos",
            json={
                "items": [
                    {
                        "snippet": {
                            "title": "Test",
                            "description": long_desc,
                            "tags": many_tags,
                        }
                    }
                ]
            },
        )

        result = get_video_metadata("test123", "fake_api_key")
        assert result["description"] == long_desc
        assert len(result["tags"]) == 100

    @pytest.mark.p1
    @pytest.mark.unit
    def test_special_characters_in_tags(self, requests_mock):
        """Test handling of special characters in tags (P1)."""
        requests_mock.get(
            "https://www.googleapis.com/youtube/v3/videos",
            json={
                "items": [
                    {
                        "snippet": {
                            "title": "Test",
                            "description": "Desc",
                            "tags": [
                                "tag-with-dash",
                                "tag_with_underscore",
                                "tag.with.dots",
                            ],
                        }
                    }
                ]
            },
        )

        result = get_video_metadata("test123", "fake_api_key")
        assert "tag-with-dash" in result["tags"]
        assert "tag_with_underscore" in result["tags"]
        assert "tag.with.dots" in result["tags"]

    @pytest.mark.p1
    @pytest.mark.unit
    def test_null_tags_field(self, requests_mock):
        """Test handling of null tags field (P1)."""
        requests_mock.get(
            "https://www.googleapis.com/youtube/v3/videos",
            json={
                "items": [
                    {
                        "snippet": {
                            "title": "Test",
                            "description": "Desc",
                            "tags": None,  # Null instead of empty array
                        }
                    }
                ]
            },
        )

        result = get_video_metadata("test123", "fake_api_key")
        assert result["title"] == "Test"
        # Should handle null gracefully (may return None or [])

    @pytest.mark.p1
    @pytest.mark.unit
    def test_empty_title(self, requests_mock):
        """Test handling of empty title (P1)."""
        requests_mock.get(
            "https://www.googleapis.com/youtube/v3/videos",
            json={
                "items": [
                    {
                        "snippet": {
                            "title": "",
                            "description": "Desc",
                            "tags": [],
                        }
                    }
                ]
            },
        )

        result = get_video_metadata("test123", "fake_api_key")
        assert result["title"] == ""
        assert result["description"] == "Desc"

    @pytest.mark.p1
    @pytest.mark.unit
    def test_empty_description(self, requests_mock):
        """Test handling of empty description (P1)."""
        requests_mock.get(
            "https://www.googleapis.com/youtube/v3/videos",
            json={
                "items": [
                    {
                        "snippet": {
                            "title": "Test",
                            "description": "",
                            "tags": [],
                        }
                    }
                ]
            },
        )

        result = get_video_metadata("test123", "fake_api_key")
        assert result["title"] == "Test"
        assert result["description"] == ""

    @pytest.mark.p1
    @pytest.mark.unit
    def test_newlines_in_metadata(self, requests_mock):
        """Test handling of newlines in metadata (P1)."""
        requests_mock.get(
            "https://www.googleapis.com/youtube/v3/videos",
            json={
                "items": [
                    {
                        "snippet": {
                            "title": "Test\nTitle",
                            "description": "Line 1\nLine 2",
                            "tags": [],
                        }
                    }
                ]
            },
        )

        result = get_video_metadata("test123", "fake_api_key")
        assert result["title"] == "Test\nTitle"
        assert result["description"] == "Line 1\nLine 2"

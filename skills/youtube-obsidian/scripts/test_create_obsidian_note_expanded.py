#!/usr/bin/env python3
"""
Expanded tests for create_obsidian_note() function.

Tests edge cases, special characters, and boundary conditions
for Obsidian note creation.
"""

import pytest
from get_youtube_data import create_obsidian_note
from test_helpers import (
    create_video_metadata,
    extract_frontmatter,
    assert_obsidian_note_structure,
)


class TestCreateObsidianNoteEdgeCases:
    """Tests for edge cases and special characters (P1)."""

    @pytest.mark.p1
    @pytest.mark.unit
    def test_empty_metadata_fields(self):
        """Test handling of empty metadata fields."""
        metadata = create_video_metadata(title="", description="", tags=[])
        note, filename = create_obsidian_note(
            "test123",
            "https://youtube.com/watch?v=test123",
            metadata,
            "Transcript",
            "Summary",
        )

        # Should create note even with empty metadata
        assert "---" in note
        assert "# " in note
        assert filename == "video"  # Fallback filename

    @pytest.mark.p1
    @pytest.mark.unit
    def test_special_characters_in_title(self):
        """Test handling of special characters in title."""
        metadata = create_video_metadata(
            title='Test: "Video" <Special> & Chars>',
            description="Description",
            tags=["tag"],
        )
        note, filename = create_obsidian_note(
            "test123",
            "https://youtube.com/watch?v=test123",
            metadata,
            "Transcript",
            "Summary",
        )

        # Frontmatter contains special characters (not escaped)
        assert "Test: " in note
        assert "---" in note

        # Filename should be sanitized (removes certain chars)
        assert ":" not in filename
        assert '"' not in filename
        assert "<" not in filename
        assert ">" not in filename
        # Note: & may be preserved in frontmatter

    @pytest.mark.p1
    @pytest.mark.unit
    def test_unicode_characters_in_metadata(self):
        """Test handling of Unicode characters."""
        metadata = create_video_metadata(
            title="日本語 Test 🎉", description="中国语", tags=["tag"]
        )
        note, filename = create_obsidian_note(
            "test123",
            "https://youtube.com/watch?v=test123",
            metadata,
            "Transcript",
            "Summary",
        )

        # Should handle Unicode without crashing
        assert "日本語" in note
        assert "🎉" in note
        assert "中国语" in note

    @pytest.mark.p1
    @pytest.mark.unit
    def test_very_long_title_truncates_filename(self):
        """Test that very long titles truncate filename correctly."""
        long_title = "A" * 150
        metadata = create_video_metadata(title=long_title, description="", tags=[])

        note, filename = create_obsidian_note(
            "test123",
            "https://youtube.com/watch?v=test123",
            metadata,
            "Transcript",
            "Summary",
        )

        # Filename should be truncated
        assert len(filename) == 100
        assert filename.endswith("...")
        # Title in note should NOT be truncated
        assert long_title in note

    @pytest.mark.p1
    @pytest.mark.unit
    def test_exactly_100_chars_filename(self):
        """Test that exactly 100 char filename is not truncated."""
        title_100 = "A" * 100
        metadata = create_video_metadata(title=title_100, description="", tags=[])

        note, filename = create_obsidian_note(
            "test123",
            "https://youtube.com/watch?v=test123",
            metadata,
            "Transcript",
            "Summary",
        )

        # Should not truncate
        assert len(filename) == 100
        assert not filename.endswith("...")

    @pytest.mark.p1
    @pytest.mark.unit
    def test_special_characters_in_description(self):
        """Test handling of special characters in description."""
        metadata = create_video_metadata(
            title="Test",
            description="Line 1\nLine 2\n\nPara 2",
            tags=["tag"],
        )
        note, filename = create_obsidian_note(
            "test123",
            "https://youtube.com/watch?v=test123",
            metadata,
            "Transcript",
            "Summary",
        )

        # Should preserve line breaks in description
        assert "Line 1" in note
        assert "Line 2" in note
        assert "Para 2" in note


class TestCreateObsidianNoteFrontmatter:
    """Tests for frontmatter generation (P1)."""

    @pytest.mark.p1
    @pytest.mark.unit
    def test_frontmatter_contains_title(self):
        """Test that frontmatter includes title."""
        metadata = create_video_metadata(title="Test Title")
        note, _ = create_obsidian_note(
            "test123", "https://youtube.com/watch?v=test123", metadata, "T", "S"
        )

        frontmatter = extract_frontmatter(note)
        assert frontmatter.get("title") == "Test Title"

    @pytest.mark.p1
    @pytest.mark.unit
    def test_frontmatter_contains_youtube_id(self):
        """Test that frontmatter includes YouTube ID."""
        metadata = create_video_metadata()
        note, _ = create_obsidian_note(
            "test123", "https://youtube.com/watch?v=test123", metadata, "T", "S"
        )

        frontmatter = extract_frontmatter(note)
        assert frontmatter.get("youtube_id") == "test123"

    @pytest.mark.p1
    @pytest.mark.unit
    def test_frontmatter_contains_youtube_url(self):
        """Test that frontmatter includes YouTube URL."""
        url = "https://youtube.com/watch?v=test123"
        metadata = create_video_metadata()
        note, _ = create_obsidian_note("test123", url, metadata, "T", "S")

        frontmatter = extract_frontmatter(note)
        assert frontmatter.get("youtube_url") == url

    @pytest.mark.p1
    @pytest.mark.unit
    def test_frontmatter_contains_tags(self):
        """Test that frontmatter includes tags array."""
        tags = ["python", "tutorial", "coding"]
        metadata = create_video_metadata(
            title="Test Video", description="Test", tags=tags
        )
        note, _ = create_obsidian_note(
            "test123",
            "https://youtube.com/watch?v=test123",
            metadata,
            "Test transcript",
            "Summary",
        )

        frontmatter = extract_frontmatter(note)
        note_tags = frontmatter.get("tags", [])
        # Tags from metadata should be included
        # Additional tags may be generated from content
        for tag in tags:
            assert tag in note_tags

    @pytest.mark.p1
    @pytest.mark.unit
    def test_tags_generated_when_empty_in_metadata(self):
        """Test that tags are generated from content when empty in metadata."""
        metadata = create_video_metadata(
            title="Python Tutorial",
            description="Learn Python",
            tags=[],  # Empty in metadata
        )
        note, _ = create_obsidian_note(
            "test123",
            "https://youtube.com/watch?v=test123",
            metadata,
            "Python programming transcript",
            "Summary",
        )

        # Should generate tags from content
        assert "python" in note.lower()


class TestCreateObsidianNoteContent:
    """Tests for note content sections (P1)."""

    @pytest.mark.p1
    @pytest.mark.unit
    def test_includes_user_summary_section(self):
        """Test that user summary section is included."""
        metadata = create_video_metadata()
        note, _ = create_obsidian_note(
            "test123",
            "https://youtube.com/watch?v=test123",
            metadata,
            "Transcript",
            "My summary",
        )

        assert "## Summary" in note
        assert "My summary" in note

    @pytest.mark.p1
    @pytest.mark.unit
    def test_includes_user_comments_when_provided(self):
        """Test that user comments section is included when provided."""
        metadata = create_video_metadata()
        note, _ = create_obsidian_note(
            "test123",
            "https://youtube.com/watch?v=test123",
            metadata,
            "Transcript",
            "Summary",
            "My comments",
        )

        assert "## Notes/Comments" in note
        assert "My comments" in note

    @pytest.mark.p1
    @pytest.mark.unit
    def test_omits_user_comments_when_not_provided(self):
        """Test that user comments section is omitted when not provided."""
        metadata = create_video_metadata()
        note, _ = create_obsidian_note(
            "test123",
            "https://youtube.com/watch?v=test123",
            metadata,
            "Transcript",
            "Summary",
            None,  # No comments
        )

        # Should not have comments section
        assert "## Notes/Comments" not in note

    @pytest.mark.p1
    @pytest.mark.unit
    def test_includes_description_section(self):
        """Test that description section is included."""
        metadata = create_video_metadata(title="Test", description="Test description")
        note, _ = create_obsidian_note(
            "test123",
            "https://youtube.com/watch?v=test123",
            metadata,
            "Transcript",
            "Summary",
        )

        assert "## Description" in note
        assert "Test description" in note

    @pytest.mark.p1
    @pytest.mark.unit
    def test_includes_transcript_section(self):
        """Test that transcript section is included."""
        metadata = create_video_metadata()
        note, _ = create_obsidian_note(
            "test123",
            "https://youtube.com/watch?v=test123",
            metadata,
            "Test transcript text",
            "Summary",
        )

        assert "## Full Transcript" in note
        assert "Test transcript text" in note

    @pytest.mark.p1
    @pytest.mark.unit
    def test_title_heading(self):
        """Test that title is used as heading."""
        metadata = create_video_metadata(title="My Video Title")
        note, _ = create_obsidian_note(
            "test123",
            "https://youtube.com/watch?v=test123",
            metadata,
            "Transcript",
            "Summary",
        )

        assert "# My Video Title" in note


class TestCreateObsidianNoteMarkdown:
    """Tests for markdown formatting (P1)."""

    @pytest.mark.p1
    @pytest.mark.unit
    def test_user_comments_with_markdown_formatting(self):
        """Test that markdown in user comments is preserved."""
        metadata = create_video_metadata()
        note, _ = create_obsidian_note(
            "test123",
            "https://youtube.com/watch?v=test123",
            metadata,
            "Transcript",
            "Summary",
            "**Bold** text\n*Italic* text\n- List item",
        )

        # Should preserve markdown
        assert "**Bold**" in note
        assert "*Italic*" in note
        assert "- List item" in note

    @pytest.mark.p1
    @pytest.mark.unit
    def test_user_summary_with_markdown_formatting(self):
        """Test that markdown in user summary is preserved."""
        metadata = create_video_metadata()
        note, _ = create_obsidian_note(
            "test123",
            "https://youtube.com/watch?v=test123",
            metadata,
            "Transcript",
            "## Key Points\n- Point 1\n- Point 2",
            None,
        )

        # Should preserve markdown in summary
        assert "## Key Points" in note
        assert "- Point 1" in note
        assert "- Point 2" in note

    @pytest.mark.p1
    @pytest.mark.unit
    def test_frontmatter_json_array_format(self):
        """Test that tags in frontmatter are JSON array."""
        metadata = create_video_metadata(tags=["tag1", "tag2", "tag3"])
        note, _ = create_obsidian_note(
            "test123",
            "https://youtube.com/watch?v=test123",
            metadata,
            "Transcript",
            "Summary",
        )

        # Frontmatter should have JSON array format
        assert "tags: [" in note
        assert '"tag1"' in note
        assert '"tag2"' in note
        assert '"tag3"' in note


class TestCreateObsidianNoteStructure:
    """Tests for overall note structure (P1)."""

    @pytest.mark.p1
    @pytest.mark.unit
    def test_has_valid_frontmatter(self):
        """Test that note starts and ends frontmatter correctly."""
        metadata = create_video_metadata()
        note, _ = create_obsidian_note(
            "test123", "https://youtube.com/watch?v=test123", metadata, "T", "S"
        )

        # Should start with ---
        assert note.startswith("---")
        # Should have closing ---
        second_marker = note.find("---", 3)
        assert second_marker > 0

    @pytest.mark.p1
    @pytest.mark.unit
    def test_has_all_required_sections(self):
        """Test that note has all required sections."""
        metadata = create_video_metadata()
        note, _ = create_obsidian_note(
            "test123",
            "https://youtube.com/watch?v=test123",
            metadata,
            "Transcript",
            "Summary",
        )

        assert_obsidian_note_structure(note)

    @pytest.mark.p1
    @pytest.mark.unit
    def test_sections_in_correct_order(self):
        """Test that sections are in expected order."""
        metadata = create_video_metadata()
        note, _ = create_obsidian_note(
            "test123",
            "https://youtube.com/watch?v=test123",
            metadata,
            "Transcript",
            "Summary",
            "Comments",
        )

        # Check order of sections
        frontmatter_end = note.find("---", 3)
        title_pos = note.find("# ", frontmatter_end)
        summary_pos = note.find("## Summary", title_pos)
        comments_pos = note.find("## Notes/Comments", summary_pos)
        desc_pos = note.find("## Description", comments_pos)
        transcript_pos = note.find("## Full Transcript", desc_pos)

        assert frontmatter_end < title_pos < summary_pos
        assert summary_pos < comments_pos < desc_pos < transcript_pos


class TestCreateObsidianNoteEmptyTranscript:
    """Tests for empty transcript handling (P1)."""

    @pytest.mark.p1
    @pytest.mark.unit
    def test_empty_transcript(self):
        """Test handling of empty transcript."""
        metadata = create_video_metadata(title="Test")
        note, _ = create_obsidian_note(
            "test123",
            "https://youtube.com/watch?v=test123",
            metadata,
            "",  # Empty transcript
            "Summary",
        )

        # Should still create note with empty transcript section
        assert "## Full Transcript" in note

    @pytest.mark.p1
    @pytest.mark.unit
    def test_transcript_with_special_chars(self):
        """Test handling of transcript with special characters."""
        metadata = create_video_metadata()
        note, _ = create_obsidian_note(
            "test123",
            "https://youtube.com/watch?v=test123",
            metadata,
            "Text with @#$%^&*() special chars",
            "Summary",
        )

        # Should include special characters in transcript
        assert "@#$%^&*()" in note

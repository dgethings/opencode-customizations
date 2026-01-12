#!/usr/bin/env python3
"""
Test helper utilities for youtube-obsidian tests.

This module provides reusable helper functions for common test patterns,
data generation, and assertion utilities.
"""

import os
import json
from typing import Any, Dict, List
from unittest.mock import Mock


def create_mock_transcript_list(
    texts: List[str], starts: List[float] = None, durations: List[float] = None
) -> List[Mock]:
    """Create a list of mock transcript entries.

    Args:
        texts: List of transcript text strings
        starts: Optional list of start times (defaults to sequential)
        durations: Optional list of durations (defaults to 1.0)

    Returns:
        List of Mock objects with text, start, and duration attributes
    """
    entries = []
    for i, text in enumerate(texts):
        entry = Mock()
        entry.text = text
        entry.start = starts[i] if starts and i < len(starts) else float(i)
        entry.duration = durations[i] if durations and i < len(durations) else 1.0
        entries.append(entry)
    return entries


def create_video_metadata(
    title: str = "Test Video",
    description: str = "Test Description",
    tags: List[str] = None,
) -> Dict[str, Any]:
    """Create video metadata dictionary.

    Args:
        title: Video title
        description: Video description
        tags: Optional list of tags

    Returns:
        Dictionary with video metadata structure
    """
    return {
        "title": title,
        "description": description,
        "tags": tags or [],
    }


def create_youtube_api_response(
    title: str = "Test Video",
    description: str = "Test Description",
    tags: List[str] = None,
) -> Dict[str, Any]:
    """Create YouTube API response structure.

    Args:
        title: Video title
        description: Video description
        tags: Optional list of tags

    Returns:
        Dictionary matching YouTube Data API v3 response format
    """
    return {
        "items": [
            {
                "snippet": create_video_metadata(title, description, tags),
            }
        ]
    }


def assert_metadata_matches(
    actual: Dict[str, Any], expected: Dict[str, Any], msg: str = None
) -> None:
    """Assert that video metadata matches expected values.

    Args:
        actual: Actual metadata dictionary
        expected: Expected metadata dictionary
        msg: Optional assertion message

    Raises:
        AssertionError: If metadata doesn't match
    """
    errors = []

    if actual.get("title") != expected.get("title"):
        errors.append(
            f"Title mismatch: expected '{expected.get('title')}', got '{actual.get('title')}'"
        )

    if actual.get("description") != expected.get("description"):
        errors.append(
            f"Description mismatch: expected '{expected.get('description')}', got '{actual.get('description')}'"
        )

    actual_tags = set(actual.get("tags", []))
    expected_tags = set(expected.get("tags", []))
    if actual_tags != expected_tags:
        errors.append(f"Tags mismatch: expected {expected_tags}, got {actual_tags}")

    if errors:
        full_msg = msg or "Metadata mismatch"
        full_msg += ":\n" + "\n".join(errors)
        raise AssertionError(full_msg)


def assert_obsidian_note_structure(note_content: str) -> None:
    """Assert that Obsidian note has required structure.

    Args:
        note_content: Full note content string

    Raises:
        AssertionError: If structure is invalid
    """
    errors = []

    # Check frontmatter
    if not note_content.startswith("---"):
        errors.append("Note must start with frontmatter (---)")
    if "---" not in note_content[4:]:  # Second frontmatter marker
        errors.append("Note must have closing frontmatter marker (---)")

    # Check required sections
    if "# " not in note_content:
        errors.append("Note must have at least one heading")
    if "## Full Transcript" not in note_content:
        errors.append("Note must have '## Full Transcript' section")

    if errors:
        raise AssertionError("Invalid note structure:\n" + "\n".join(errors))


def extract_frontmatter(note_content: str) -> Dict[str, Any]:
    """Extract frontmatter from Obsidian note.

    Args:
        note_content: Full note content string

    Returns:
        Dictionary with frontmatter key-value pairs
    """
    if not note_content.startswith("---"):
        return {}

    end_idx = note_content.find("---", 3)
    if end_idx == -1:
        return {}

    frontmatter_text = note_content[3:end_idx].strip()
    frontmatter = {}

    for line in frontmatter_text.split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()

            # Try to parse as JSON (for tags array)
            try:
                value = json.loads(value)
            except (json.JSONDecodeError, ValueError):
                pass

            frontmatter[key] = value

    return frontmatter


def assert_tags_contain_expected(
    actual_tags: List[str], expected_tags: List[str], allow_extra: bool = True
) -> None:
    """Assert that actual tags contain expected tags.

    Args:
        actual_tags: List of actual tags
        expected_tags: List of expected tags that must be present
        allow_extra: If True, allow additional tags in actual_tags

    Raises:
        AssertionError: If expected tags are missing
    """
    actual_set = set(actual_tags)
    expected_set = set(expected_tags)

    missing = expected_set - actual_set

    if missing:
        msg = f"Missing expected tags: {missing}"
        if not allow_extra:
            extra = actual_set - expected_set
            if extra:
                msg += f"\nUnexpected extra tags: {extra}"
        raise AssertionError(msg)


def count_tag_occurrences(tags: List[str]) -> Dict[str, int]:
    """Count occurrences of each tag in a list.

    Args:
        tags: List of tags (may contain duplicates)

    Returns:
        Dictionary mapping tag to count
    """
    counts: Dict[str, int] = {}
    for tag in tags:
        counts[tag] = counts.get(tag, 0) + 1
    return counts


def assert_no_duplicate_tags(tags: List[str]) -> None:
    """Assert that there are no duplicate tags in a list.

    Args:
        tags: List of tags

    Raises:
        AssertionError: If duplicates found
    """
    counts = count_tag_occurrences(tags)
    duplicates = {tag: count for tag, count in counts.items() if count > 1}

    if duplicates:
        raise AssertionError(f"Duplicate tags found: {duplicates}")


def create_test_file_content(
    video_id: str = "test123",
    url: str = "https://youtube.com/watch?v=test123",
    metadata: Dict[str, Any] = None,
    transcript: str = "Test transcript",
    user_summary: str = "Test summary",
    user_comments: str = None,
) -> str:
    """Create a test Obsidian note content.

    Helper for creating expected note content in tests.

    Args:
        video_id: YouTube video ID
        url: YouTube URL
        metadata: Video metadata (uses defaults if None)
        transcript: Transcript text
        user_summary: User summary section
        user_comments: Optional user comments section

    Returns:
        Full note content as string
    """
    if metadata is None:
        metadata = create_video_metadata()

    tags = metadata.get("tags", [])

    frontmatter = f"""---
title: {metadata["title"]}
youtube_id: {video_id}
tags: {json.dumps(tags)}
youtube_url: {url}
---

"""

    content = f"""# {metadata["title"]}

## Summary
{user_summary}

"""

    if user_comments:
        content += f"""## Notes/Comments
{user_comments}

"""

    content += f"""## Description
{metadata["description"]}

## Full Transcript
{transcript}
"""

    return frontmatter + content


def parse_obsidian_file(file_path: str) -> Dict[str, Any]:
    """Parse an Obsidian markdown file into components.

    Args:
        file_path: Path to the markdown file

    Returns:
        Dictionary with components: frontmatter, title, summary, comments, description, transcript
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    frontmatter = extract_frontmatter(content)
    body = content[content.find("---", 3) + 3 :].strip()

    components = {
        "frontmatter": frontmatter,
        "body": body,
    }

    # Extract title from heading
    if "# " in body:
        title_line = body.split("\n")[0]
        components["title"] = title_line.replace("# ", "").strip()

    # Extract sections
    if "## Summary" in body:
        summary_section = body.split("## Summary")[1]
        if "##" in summary_section:
            components["summary"] = summary_section.split("##")[0].strip()
        else:
            components["summary"] = summary_section.strip()

    if "## Notes/Comments" in body:
        comments_section = body.split("## Notes/Comments")[1]
        if "##" in comments_section:
            components["comments"] = comments_section.split("##")[0].strip()
        else:
            components["comments"] = comments_section.strip()

    if "## Description" in body:
        desc_section = body.split("## Description")[1]
        if "##" in desc_section:
            components["description"] = desc_section.split("##")[0].strip()
        else:
            components["description"] = desc_section.strip()

    if "## Full Transcript" in body:
        transcript_section = body.split("## Full Transcript")[1]
        components["transcript"] = transcript_section.strip()

    return components


def validate_file_created(directory: str, filename: str) -> str:
    """Validate that a file was created in directory.

    Args:
        directory: Directory path
        filename: Expected filename

    Returns:
        Full file path

    Raises:
        AssertionError: If file doesn't exist
    """
    file_path = os.path.join(directory, filename)

    if not os.path.exists(file_path):
        files = os.listdir(directory) if os.path.exists(directory) else []
        raise AssertionError(
            f"File not created: {filename}\n"
            f"Directory: {directory}\n"
            f"Files found: {files}"
        )

    return file_path


def create_long_string(length: int) -> str:
    """Create a string of specified length.

    Args:
        length: Desired string length

    Returns:
        String of length 'length' filled with 'A'
    """
    return "A" * length

#!/usr/bin/env python3
import os
import re
import json
import sys
from urllib.parse import urlparse, parse_qs

try:
    import requests
except ImportError:
    print("Error: requests module not found. Install with: pip install requests")
    sys.exit(1)

try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    print(
        "Error: youtube-transcript-api not found. Install with: pip install youtube-transcript-api"
    )
    sys.exit(1)


def extract_video_id(url):
    """Extract YouTube video ID from various URL formats."""
    patterns = [
        r"(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/|youtube\.com\/v\/)([^&\n?#]+)",
        r"^([a-zA-Z0-9_-]{11})$",
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    raise ValueError(f"Could not extract video ID from URL: {url}")


def get_video_metadata(video_id, api_key):
    """Fetch video title, description, and tags from YouTube Data API."""
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "snippet",
        "id": video_id,
        "key": api_key,
        "fields": "items(snippet(title,description,tags))",
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()

    if not data.get("items"):
        raise ValueError(f"Video not found: {video_id}")

    snippet = data["items"][0]["snippet"]
    return {
        "title": snippet.get("title", ""),
        "description": snippet.get("description", ""),
        "tags": snippet.get("tags", []),
    }


def get_transcript(video_id):
    """Fetch full transcript for the video."""
    try:
        api = YouTubeTranscriptApi()
        transcript_list = api.fetch(video_id)
        transcript = " ".join([entry.text for entry in transcript_list])
        return transcript
    except Exception as e:
        raise ValueError(f"Could not fetch transcript: {e}")


def generate_tags(title, description, transcript, youtube_tags=None):
    """Generate relevant tags from video content."""
    tags = set()

    if youtube_tags:
        tags.update(youtube_tags)

    content = f"{title} {description} {transcript}"

    keywords = re.findall(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b", content)
    for kw in keywords[:10]:
        tag = kw.lower()
        if len(tag) > 3:
            tags.add(tag)

    common_tech_terms = [
        "python",
        "javascript",
        "ai",
        "machine learning",
        "programming",
        "development",
        "software",
        "api",
        "data",
        "web",
        "frontend",
        "backend",
        "cloud",
        "docker",
        "kubernetes",
        "tutorial",
        "guide",
        "youtube",
        "video",
        "learning",
        "course",
        "tips",
        "best practices",
    ]

    lower_content = content.lower()
    for term in common_tech_terms:
        if term in lower_content:
            tags.add(term)

    return sorted(list(tags))[:15]


def sanitize_filename(title):
    """Sanitize video title for use as filename."""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        title = title.replace(char, "")
    title = title.strip()

    if len(title) > 100:
        title = title[:97] + "..."

    return title or "video"


def create_obsidian_note(
    video_id, url, metadata, transcript, user_summary, user_comments=None
):
    """Create Obsidian markdown note with frontmatter and content."""
    title = metadata["title"]
    description = metadata["description"]
    youtube_tags = metadata.get("tags", [])

    tags = generate_tags(title, description, transcript, youtube_tags)

    frontmatter = f"""---
title: {title}
youtube_id: {video_id}
tags: {json.dumps(tags)}
youtube_url: {url}
---

"""

    content = f"""# {title}

## Summary
{user_summary}

"""

    if user_comments:
        content += f"""## Notes/Comments
{user_comments}

"""

    content += f"""## Description
{description}

## Full Transcript
{transcript}
"""

    return frontmatter + content, sanitize_filename(title)


def main():
    if len(sys.argv) < 2:
        print(
            "Usage: python get_youtube_data.py <youtube_url> [user_summary] [user_comments]"
        )
        print("Environment variables needed:")
        print("  YOUTUBE_API_KEY - Your YouTube Data API v3 key")
        print("  OBSIDIAN_VAULT_PATH - Path to your Obsidian vault")
        sys.exit(1)

    youtube_url = sys.argv[1]
    user_summary = sys.argv[2] if len(sys.argv) > 2 else ""
    user_comments = sys.argv[3] if len(sys.argv) > 3 else ""

    api_key = os.environ.get("YOUTUBE_API_KEY")
    if not api_key:
        print("Error: YOUTUBE_API_KEY environment variable not set")
        sys.exit(1)

    vault_path = os.environ.get("VAULT_PATH") or os.environ.get("OBSIDIAN_VAULT_PATH")
    if not vault_path:
        print("Error: VAULT_PATH or OBSIDIAN_VAULT_PATH environment variable not set")
        sys.exit(1)

    try:
        video_id = extract_video_id(youtube_url)
        print(f"Extracted video ID: {video_id}")

        print("Fetching video metadata...")
        metadata = get_video_metadata(video_id, api_key)
        print(f"Title: {metadata['title']}")

        print("Fetching transcript...")
        transcript = get_transcript(video_id)
        print(f"Transcript length: {len(transcript)} characters")

        print("Generating Obsidian note...")
        note_content, filename = create_obsidian_note(
            video_id, youtube_url, metadata, transcript, user_summary, user_comments
        )

        output_path = os.path.join(vault_path, f"{filename}.md")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(note_content)

        print(f"✅ Obsidian note created: {output_path}")
        print(f"   Filename: {filename}.md")
        print(f"   Tags: {metadata.get('tags', [])}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

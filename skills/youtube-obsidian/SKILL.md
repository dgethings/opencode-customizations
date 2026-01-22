---
name: capture-youtube-insight
description: "Extract YouTube video metadata and transcripts to create Obsidian markdown notes. Use for creating structured notes from YouTube videos, saving video transcripts with metadata for future reference, and generating tagged notes from YouTube content including title, description, and transcript. Requires YOUTUBE_API_KEY and VAULT_PATH environment variables."
---

# YouTube to Obsidian

Extract YouTube video content and create structured Obsidian notes with frontmatter.

## Prerequisites

Set these environment variables:

```bash
export YOUTUBE_API_KEY="your-youtube-data-api-v3-key"
export VAULT_PATH="/path/to/your/obsidian/vault"
```

**YouTube API Key**: Get from https://console.cloud.google.com/
- Create project, enable YouTube Data API v3
- Create API key in Credentials section

**Python Dependencies**:
```bash
pip install requests youtube-transcript-api
```

## Workflow

### 1. Extract Video Information

Run the script to fetch all video data:

```bash
uv run scripts/get_youtube_data.py <youtube_url> "<user_summary>" "<user_comments>"
```

**Parameters**:
- `youtube_url`: Full YouTube URL or video ID
- `user_summary` (optional): Your summary of the video
- `user_comments` (optional): Your personal notes/comments

**Example**:
```bash
uv run scripts/get_youtube_data.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" "A classic music video" "Remember this from 1987"
```

### 2. Script Execution

The script automatically:
- Extracts video ID from URL
- Fetches title, description, and tags via YouTube Data API
- Retrieves full transcript using youtube-transcript-api
- Auto-generates relevant tags from content
- Creates Obsidian markdown file with proper frontmatter
- Saves note to your vault

**Note Filename**: Sanitized video title (first 100 chars, special characters removed)

### 3. Obsidian Note Structure

**Frontmatter**:
```yaml
---
title: Video Title
youtube_id: dQw4w9WgXcQ
tags: ["music", "video", "classic"]
youtube_url: https://www.youtube.com/watch?v=dQw4w9WgXcQ
---
```

**Content**:
- Summary section (from user input)
- Notes/Comments section (from user input, optional)
- Description section (from YouTube metadata)
- Full transcript section

## Tag Generation

Tags are auto-generated from:
1. YouTube's video tags (if available)
2. Capitalized words in title, description, transcript
3. Common technical terms found in content

Maximum 5 tags per note.

## Error Handling

**Video ID extraction fails**: Check URL format (supports youtube.com/watch?v=..., youtu.be/..., youtube.com/embed/)

**Metadata fetch fails**: Verify YOUTUBE_API_KEY is valid and has YouTube Data API v3 enabled

**Transcript unavailable**: Some videos have disabled captions. The script will report this error.

**Vault path invalid**: Ensure VAULT_PATH points to existing directory with write permissions

## Manual Summarization

The script creates the Obsidian note with all data, but does NOT auto-summarize the transcript. The user must provide their own summary.

After the note is created, you may want to ask Claude to summarize the transcript content and update the note.


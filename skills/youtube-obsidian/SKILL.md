---
name: capture-youtube-insight
description: "Extract YouTube video metadata and transcripts to create Obsidian markdown notes. Use for creating structured notes from YouTube videos, saving video transcripts with metadata for future reference, and generating tagged notes from YouTube content including title, description, and transcript. Requires YOUTUBE_API_KEY and VAULT_PATH environment variables."
---

# YouTube to Obsidian

Extract YouTube video content and create structured Obsidian notes with frontmatter.

## Prerequisites

You maybe given some comments from the user about the video. This will be given with the YouTube video ID or URL. If the user does give comments then save this as `user_comments` for later steps.

## Workflow

### 1. Extract Video Information

Run the script to fetch all video data:

```bash
uv run scripts/yt.py metadata <youtube_url>
```

**Parameters**:
- `youtube_url`: Full YouTube URL or video ID

**Example**:
```bash
uv run scripts/yt.py metadata "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### 2. Script Execution

The script automatically:
- Extracts video ID from URL
- Fetches title and description via YouTube Data API
- Retrieves full transcript using youtube-transcript-api
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


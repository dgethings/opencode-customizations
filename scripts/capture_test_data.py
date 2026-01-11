#!/usr/bin/env python3
import os
import sys
import json

sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "skills", "youtube-obsidian", "scripts")
)

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


def main():
    if len(sys.argv) < 2:
        print("Usage: python capture_test_data.py <youtube_url>")
        print("Environment variables needed:")
        print("  YOUTUBE_API_KEY - Your YouTube Data API v3 key")
        sys.exit(1)

    youtube_url = sys.argv[1]

    api_key = os.environ.get("YOUTUBE_API_KEY")
    if not api_key:
        print("Error: YOUTUBE_API_KEY environment variable not set")
        sys.exit(1)

    try:
        from get_youtube_data import extract_video_id

        video_id = extract_video_id(youtube_url)
        print(f"Extracted video ID: {video_id}")

        print("Fetching video metadata...")
        metadata = get_video_metadata(video_id, api_key)
        print(f"Title: {metadata['title']}")

        print("Fetching transcript...")
        transcript = get_transcript(video_id)
        print(f"Transcript length: {len(transcript)} characters")

        test_data_dir = os.path.join(
            os.path.dirname(__file__), "skills", "youtube-obsidian", "test_data"
        )
        os.makedirs(test_data_dir, exist_ok=True)

        mock_api_file = os.path.join(test_data_dir, "mock_youtube_api_response.json")
        with open(mock_api_file, "w", encoding="utf-8") as f:
            json.dump(
                {"items": [{"snippet": metadata}]}, f, indent=2, ensure_ascii=False
            )
        print(f"Saved mock API response to: {mock_api_file}")

        mock_transcript_file = os.path.join(test_data_dir, "mock_transcript.json")
        with open(mock_transcript_file, "w", encoding="utf-8") as f:
            json.dump({"transcript": transcript}, f, indent=2, ensure_ascii=False)
        print(f"Saved mock transcript to: {mock_transcript_file}")

        test_cases_file = os.path.join(test_data_dir, "test_cases.json")
        test_cases = [
            {
                "name": "Standard Watch URL",
                "url": youtube_url,
                "video_id": video_id,
                "expected_title": metadata["title"],
            }
        ]
        with open(test_cases_file, "w", encoding="utf-8") as f:
            json.dump(test_cases, f, indent=2, ensure_ascii=False)
        print(f"Saved test cases to: {test_cases_file}")

        print("\n✅ Test data captured successfully!")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

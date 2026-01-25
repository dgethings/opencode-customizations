import os
from functools import reduce
from typing import Annotated, Literal

import requests
from pydantic import AnyUrl, BaseModel
from typer import Argument, Exit, Option, Typer, echo
from youtube_transcript_api import VideoUnavailable, YouTubeTranscriptApi

app = Typer()


# types
class Params(BaseModel):
    part: str = "snippet"
    id: str
    key: str
    fields: str = "items(snippet(title,description,tags))"


class Snippet(BaseModel):
    title: str
    description: str


YTDataApiURL = "https://www.googleapis.com/youtube/v3/videos"


# helper functions
def fetch_transcript(id: str, langs=["en"]) -> str:
    """Fetch and concatenate transcript segments for a YouTube video.

    Args:
        id: YouTube video ID
        langs: List of language codes to fetch transcript in (default: ["en"])

    Returns:
        Concatenated transcript text as a single string
    """
    api = YouTubeTranscriptApi()
    try:
        fetched = api.fetch(id, langs)
    except VideoUnavailable as err:
        echo(err)
        raise Exit(1)
    except Exception as e:
        echo(e)
        raise Exit(2)

    t = reduce(lambda t, x: f"{t}{x.text} ", fetched, "")
    return t


def parse_yt_url(url: str) -> AnyUrl:
    """Validate and parse a YouTube URL using Pydantic's AnyUrl type.

    Args:
        url: YouTube video URL string

    Returns:
        Validated AnyUrl object for the YouTube video
    """
    return AnyUrl(url)


def yt_data_api(id: str, url=YTDataApiURL, api_key: str | None = None) -> Snippet:
    """Get video metadata using YT data API."""
    api_key = api_key or os.environ.get("YOUTUBE_API_KEY")
    if not api_key:
        echo("Environment variable YOUTUBE_API_KEY is required to get Youtube metadata")
        raise Exit(4)

    response = requests.get(url, params=Params(id=id, key=api_key))
    response.raise_for_status()

    data = response.json()

    if not data.get("items"):
        raise ValueError(f"Video not found: {id}")

    try:
        snippet = data["items"][0]["snippet"]
    except (KeyError, IndexError):
        echo(f"Video {id} did not contain the `snippet` metadata field. Got: {data}")
        raise Exit(5)

    return Snippet(title=snippet.get("title"), description=snippet.get("description"))


def get_metadata(id: str) -> str:
    """Fetch video title and description from YouTube Data API."""
    return yt_data_api(id).model_dump_json()


# cli argument definitions
ID = Annotated[str, Argument(help="Youtube video ID")]
LANG = Annotated[str, Option(help="language you want the transcript in")]
URL = Annotated[AnyUrl, Argument(help="Youtube URL", parser=parse_yt_url)]


@app.command()
def transcript(id: ID, lang: LANG = "en") -> None:
    """Fetch the transcript for the given video ID."""
    echo(fetch_transcript(id, [lang]))


@app.command()
def id(url: URL) -> None:
    """Return the Youtube video ID from a given YouTube URL"""
    id = [x[1] for x in url.query_params() if x[0] == "v"]
    if not id:
        echo(f"{url} missing the 'v' parameter that contains the video ID")
        raise Exit(3)
    echo(id[0])


@app.command()
def metadata(id: Annotated[str, Argument(help="YouTube video ID")]) -> None:
    """Returns the video title and description for a given YouTube video ID"""
    echo(get_metadata(id))


if __name__ == "__main__":
    app()

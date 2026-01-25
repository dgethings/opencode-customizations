# // script
# dependencies = [
#     "typer>=0.21.*"
#     "youtube-transcript-api>=1.2.3"
# ]
# //
from functools import reduce
from typing import Annotated

from typer import Argument, Exit, Option, Typer, echo
from youtube_transcript_api import VideoUnavailable, YouTubeTranscriptApi

app = Typer()


def fetch_transcript(id: str, langs=["en"]) -> str:
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


@app.command()
def transcript(
    id: Annotated[str, Argument(help="Youtube video ID")],
    lang: Annotated[str, Option(help="language you want the transcript in")] = "en",
) -> None:
    echo(fetch_transcript(id, [lang]))


if __name__ == "__main__":
    app()

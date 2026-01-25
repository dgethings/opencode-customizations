import json
import os
import re
from datetime import date
from pathlib import Path
from typing import Annotated, ClassVar

from pydantic import AnyUrl, BaseModel
from typer import Argument, Exit, Typer, echo

app = Typer()


def sanitize_filename(title: str) -> str:
    """Sanitize video title for use as filename."""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        title = title.replace(char, "")
    title = title.strip()
    title = title.rstrip(".")

    if len(title) > 100:
        title = title[:97] + "..."

    return title or "video"


def generate_tags(
    title: str, description: str, transcript: str, youtube_tags: list[str] | None = None
) -> list[str]:
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

    return sorted(list(tags))[:5]


class Data(BaseModel):
    id: str
    title: str
    description: str
    tags: list[str]
    user_comments: str
    summary: str
    url: AnyUrl
    transcript: str
    today: ClassVar[date] = date.today()


def metadata(file: str) -> Data:
    """Parse JSON file and return Data model instance."""
    try:
        return Data(**json.loads(Path(file).read_text()))
    except ValueError as err:
        echo(err)
        raise Exit(1)


def write_note(filename: str, contents: str) -> None:
    """Write contents to a file in the vault."""
    vault_path = os.getenv("VAULT_PATH")
    if not vault_path:
        echo("env var VAULT_PATH not set, cannot write file")
        raise Exit(2)
    file = Path(vault_path) / filename
    file.write_text(contents)


def yt_template(data: Data) -> str:
    """Generate Obsidian markdown note template with frontmatter."""
    note = f"""---
title: {data.title}
youtube_id: {data.id}
tags: {json.dumps(data.tags)}
youtube_url: {data.url}
created: {data.today}
---

# {data.title}

"""
    if data.user_comments:
        note += f"""
## Comments
{data.user_comments}
"""
    note += f"""

## Description
{data.description}

## Transcript
{data.transcript}
"""
    return note


file = Annotated[
    Data,
    Argument(help="JSON file that contains the necessary metadata", parser=metadata),
]


@app.command()
def create_obsidian_note(data: file) -> None:
    """Create Obsidian markdown note with frontmatter and content."""
    filename = f"{data.title}.md"
    contents = yt_template(data)
    write_note(filename, contents)


if __name__ == "__main__":
    app()

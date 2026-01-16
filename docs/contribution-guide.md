# Contribution Guide

## Overview

Thank you for your interest in contributing to opencode-customizations! This guide covers how to contribute effectively to this project.

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Bun (for JavaScript/TypeScript)
- uv (Python package manager)
- Git
- GitHub account

### Fork and Clone

1. **Fork the repository** on GitHub
2. **Clone your fork:**

```bash
git clone https://github.com/<your-username>/opencode-customizations.git
cd opencode-customizations
```

3. **Add upstream remote:**

```bash
git remote add upstream https://github.com/<original-username>/opencode-customizations.git
```

### Setup Development Environment

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv pip install -e ".[test]"

# Install JavaScript dependencies
bun install
```

## Development Workflow

### Branch Strategy

**Branch Naming:**

- Feature: `feature/<feature-name>`
- Bugfix: `fix/<bug-description>`
- Refactor: `refactor/<what-refactored>`
- Documentation: `docs/<what-documented>`
- Test: `test/<what-tested>`
- Chore: `chore/<task-description>`

**Examples:**

```bash
git checkout -b feature/add-transcript-skill
git checkout -b fix/api-authentication-error
git checkout -b docs/update-readme
git checkout -b refactor/simplify-data-processing
```

### Making Changes

1. **Create feature branch:**

```bash
git checkout -b feature/your-feature-name
```

2. **Make your changes**
3. **Write tests** for your changes
4. **Run tests** to ensure they pass
5. **Lint and format** your code
6. **Commit** your changes

### Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `perf`: Performance improvements
- `ci`: CI/CD changes

**Examples:**

```
feat(youtube-obsidian): add video duration extraction

Add support for extracting video duration from YouTube metadata.
This information is now included in the Obsidian note frontmatter.

Closes #123
```

```
fix(youtube-obsidian): handle missing transcript gracefully

When a video has disabled captions, the script now displays
a clear error message instead of crashing.

Fixes #456
```

```
docs(readme): update setup instructions

Clarify installation steps and add troubleshooting section.
```

### Testing

**Write Tests First (TDD):**

1. Write failing test
2. Implement code to make test pass
3. Run tests
4. Refactor if needed

**Test Requirements:**

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest skills/youtube-obsidian/scripts/test_get_youtube_data.py -v

# Run with coverage
uv run pytest --cov=skills/youtube-obsidian/scripts --cov-report=term-missing

# Ensure 80%+ coverage
uv run pytest --cov=skills/youtube-obsidian/scripts --cov-fail-under=80
```

**Test Coverage:**

- Minimum 80% coverage required
- Test both success and failure paths
- Test edge cases and boundary conditions
- Use descriptive test names

**Example Test:**

```python
def test_extract_video_id_standard_url():
    """Test extraction of video ID from standard YouTube URL."""
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    expected = "dQw4w9WgXcQ"
    result = extract_video_id(url)
    assert result == expected
```

### Code Quality

**Linting:**

```bash
# Check for linting errors
uv run ruff check .

# Auto-fix linting issues
uv run ruff check --fix .
```

**Formatting:**

```bash
# Format code
uv run ruff format .

# Check format without modifying
uv run ruff format --check .
```

**Type Checking:**

```bash
# Run type checker
basedpyright
```

**Before Committing:**

Ensure all of the following pass:
- ✅ All tests pass
- ✅ Coverage ≥ 80%
- ✅ No linting errors
- ✅ Code formatted
- ✅ Type checking passes (if applicable)

### Pull Request Process

1. **Update your fork:**

```bash
git fetch upstream
git rebase upstream/main
```

2. **Push to your fork:**

```bash
git push origin feature/your-feature-name
```

3. **Create Pull Request:**

- Go to your fork on GitHub
- Click "Contribute" → "Open pull request"
- Fill in PR template
- Link to related issues (e.g., "Closes #123")

4. **PR Title:** Use conventional commit format

   ```
   feat(youtube-obsidian): add video duration extraction
   ```

5. **PR Description:** Include:

   - What changes were made and why
   - How to test the changes
   - Any breaking changes
   - Screenshots (if applicable)
   - Related issues

6. **Wait for review**
7. **Address review feedback**
8. **Make requested changes**
9. **Wait for approval**

### PR Review Guidelines

**For Reviewers:**

1. Check if changes align with project goals
2. Verify tests are adequate
3. Check code quality (linting, formatting, style)
4. Ensure documentation is updated
5. Test the changes locally
6. Provide constructive feedback

**For Contributors:**

1. Respond to all review comments
2. Make requested changes or explain why not
3. Be polite and respectful
4. Ask questions if something is unclear
5. Thank reviewers for their time

## Code Style Guidelines

### Python

**Imports:**

```python
# Standard library first
import os, sys, json, re
from pathlib import Path

# Third-party imports with try/except
try:
    import requests
except ImportError:
    print("Error: requests module not found. Install with: uv add requests")
    sys.exit(1)

# Local imports
from .helpers import extract_video_id
```

**Formatting:**

- 4-space indentation
- 88 character line limit
- f-strings for string formatting
- Shebang: `#!/usr/bin/env python3`

**Naming:**

- Functions: `snake_case` (e.g., `extract_video_id`)
- Classes: `PascalCase` (e.g., `VideoProcessor`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_TAGS = 15`)
- Variables: `snake_case` (e.g., `video_url`)

**Docstrings:**

```python
def extract_video_id(url: str) -> str:
    """
    Extract YouTube video ID from various URL formats.

    Supports:
    - Standard: https://www.youtube.com/watch?v=VIDEO_ID
    - Short: https://youtu.be/VIDEO_ID
    - Embed: https://www.youtube.com/embed/VIDEO_ID

    Args:
        url: YouTube video URL

    Returns:
        Video ID as string

    Raises:
        ValueError: If URL format is invalid or video ID cannot be extracted
    """
    pass
```

**Error Handling:**

```python
# Check environment variables
api_key = os.environ.get("YOUTUBE_API_KEY")
if not api_key:
    print("Error: YOUTUBE_API_KEY environment variable not set")
    sys.exit(1)

# Specific exceptions with helpful messages
try:
    response = requests.get(url)
except requests.RequestException as e:
    print(f"Error fetching data: {e}")
    sys.exit(1)

# Wrap external API calls
try:
    video_data = fetch_video_metadata(video_id)
except Exception as e:
    logger.error(f"Failed to fetch video metadata: {e}")
    raise
```

**File Operations:**

```python
# Always use context manager with encoding
with open(output_path, "w", encoding="utf-8") as f:
    f.write(content)

# Reading with encoding
with open(input_path, "r", encoding="utf-8") as f:
    content = f.read()
```

**Type Hints:**

```python
from typing import Optional, List, Dict

def process_videos(
    urls: List[str],
    max_results: Optional[int] = None
) -> Dict[str, str]:
    """Process a list of video URLs."""
    pass
```

### TypeScript

**Imports:**

```typescript
// Group imports: standard lib → third-party → relative
import { readFile, writeFile } from 'fs/promises';
import axios from 'axios';
import { extractVideoId } from './helpers';
```

**Formatting:**

- 2-space indentation
- Template literals for strings
- Prefer `const` over `let`
- Avoid `var`

**Naming:**

- Functions/variables: `camelCase` (e.g., `extractVideoId`)
- Classes: `PascalCase` (e.g., `VideoProcessor`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_TAGS = 15`)

**Error Handling:**

```typescript
try {
  const result = await fetchData(url);
  return result;
} catch (error) {
  console.error(`Error: ${error.message}`);
  throw error;
}
```

## Adding New Skills

### Skill Structure

```
skills/<skill-name>/
├── scripts/              # Python implementation
│   ├── main.py         # Entry point
│   ├── test_main.py     # Tests
│   └── conftest.py    # Pytest config
├── test_data/           # Test fixtures
└── SKILL.md            # Skill documentation
```

### Step-by-Step Guide

1. **Create skill directory:**

```bash
mkdir skills/<skill-name>
cd skills/<skill-name>
mkdir scripts
mkdir test_data
touch SKILL.md
```

2. **Add SKILL.md with frontmatter:**

```markdown
---
name: skill-name
description: "Brief description of what the skill does"
---

# Skill Name

## Description

Detailed description of the skill and its purpose.

## Prerequisites

- Required software
- API keys or credentials
- Environment variables

## Usage

```bash
uv run scripts/main.py <args>
```

## Testing

```bash
uv run pytest scripts/test_main.py -v
```

## API Reference

Documentation for functions and classes.
```

3. **Implement main script:**

```python
#!/usr/bin/env python3
"""Main script for skill-name."""

import os
import sys

def main():
    """Main entry point."""
    # Implementation
    pass

if __name__ == "__main__":
    main()
```

4. **Write tests:**

```python
"""Tests for main.py."""

import pytest
from main import your_function

def test_your_function():
    """Test your_function."""
    result = your_function(input_data)
    assert result == expected_output
```

5. **Add dependencies:**

```bash
cd ../../
uv add <package-name>
```

6. **Run tests:**

```bash
uv run pytest skills/<skill-name>/scripts/test_main.py -v
```

7. **Ensure 80%+ coverage:**

```bash
uv run pytest skills/<skill-name>/scripts/test_main.py \
  --cov=skills/<skill-name>/scripts \
  --cov-fail-under=80
```

8. **Lint and format:**

```bash
uv run ruff check skills/<skill-name>/scripts/
uv run ruff format skills/<skill-name>/scripts/
```

## Documentation

### Skill Documentation

Every skill must have a `SKILL.md` file with:

- YAML frontmatter (name, description)
- Prerequisites section
- Usage instructions
- API reference
- Testing instructions
- Error handling guide

### Project Documentation

When adding new features:

- Update relevant documentation files
- Add examples to README if applicable
- Update AGENTS.md with new commands
- Document environment variables

### Code Comments

- Add docstrings to all functions and classes
- Comment complex logic
- Explain non-obvious algorithms
- Keep comments up to date

## Security Guidelines

### Never Commit Secrets

- ❌ API keys
- ❌ Passwords
- ❌ Tokens
- ❌ Credentials

**Use Environment Variables:**

```python
# Check environment variables
api_key = os.environ.get("YOUTUBE_API_KEY")
if not api_key:
    print("Error: YOUTUBE_API_KEY not set")
    sys.exit(1)
```

### Input Validation

```python
def extract_video_id(url: str) -> str:
    """Extract and validate video ID."""
    if not url or not isinstance(url, str):
        raise ValueError("URL must be a non-empty string")
    
    # Extract and validate
    video_id = _extract_id_from_url(url)
    if not video_id:
        raise ValueError(f"Could not extract video ID from URL: {url}")
    
    return video_id
```

### Dependency Management

- Keep dependencies up to date
- Review security advisories
- Use GitHub Dependabot (if enabled)

## Issue Reporting

### Before Reporting

1. Search existing issues
2. Check if issue is already addressed
3. Verify you're using the latest version

### Reporting an Issue

1. Use GitHub issue template (if available)
2. Provide clear title
3. Describe the issue in detail
4. Include steps to reproduce
5. Provide expected vs actual behavior
6. Include environment information:
   - Python version
   - OS
   - Relevant package versions

### Bug Report Template

```markdown
**Description:**
Brief description of the bug.

**Steps to Reproduce:**
1. Step one
2. Step two
3. Step three

**Expected Behavior:**
What should happen.

**Actual Behavior:**
What actually happens.

**Environment:**
- Python version: 3.11.x
- OS: macOS/Linux/Windows
- Package version: x.x.x

**Additional Context:**
Logs, screenshots, etc.
```

### Feature Request Template

```markdown
**Description:**
Brief description of the feature.

**Problem:**
What problem does this solve?

**Proposed Solution:**
How should this be implemented?

**Alternatives:**
What other solutions did you consider?

**Additional Context:**
Any other relevant information.
```

## Questions and Support

### Getting Help

- Check existing documentation
- Search existing issues
- Ask questions in GitHub Discussions (if enabled)
- Contact maintainers directly

### Communication

- Be respectful and professional
- Provide context and details
- Be patient with responses
- Help others when you can

## Recognition

Contributors will be recognized in:

- README.md (Contributors section)
- GitHub Contributors list
- Release notes

## Code of Conduct

### Be Respectful

- Treat others with respect
- Welcome newcomers
- Be inclusive
- Use inclusive language

### Be Constructive

- Provide constructive feedback
- Focus on what is best for the community
- Show empathy toward other community members

### Be Professional

- Keep discussions professional
- Avoid personal attacks
- Focus on issues, not individuals

### Violations

Report violations to maintainers. Violations may result in:

- Warning
- Temporary suspension
- Permanent ban

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

## Summary

| Aspect | Guidelines |
|---------|------------|
| **Branch naming** | `feature/`, `fix/`, `docs/`, etc. |
| **Commit messages** | Conventional commits format |
| **Test coverage** | Minimum 80% |
| **Code quality** | Linting, formatting, type checking |
| **PR process** | Update fork, push, create PR, wait for review |
| **Documentation** | SKILL.md for skills, code comments |
| **Security** | Never commit secrets, use environment variables |
| **Communication** | Be respectful, professional, constructive |

Thank you for contributing! 🚀

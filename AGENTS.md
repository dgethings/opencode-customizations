# Opencode Customizations - Agent Guidelines

## Project Overview

This repository contains customizations for [Opencode](https://opencode.ai/), including skills, evaluation frameworks, and utilities for automating workflows.

**Key Components:**

- **Skills**: Reusable packages that extend Opencode capabilities
- **Scripts**: Python utilities within each skill
- **Evals**: Automated testing framework for skill evaluation
- **Tests**: Unit tests for skill components

## Build, Lint, Test Commands

### Python Projects

**Install dependencies**:
```bash
uv add <package>                # Add new dependency
uv pip install -r requirements.txt  # Alternative method
```

**Run scripts**:
```bash
uv run scripts/<script_name>.py <args>  # Run from project root
```

**Testing**:
```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest <path>/test_*.py

# Run specific test class or function
uv run pytest <path>/test_*.py::<TestClass>
uv run pytest -k "<test_name>"

# Run with coverage (configured in pyproject.toml)
uv run pytest --cov=scripts --cov-report=html
```

**Code Quality**:
```bash
# Linting
uv run ruff check .

# Formatting
uv run ruff format .

# Type checking
basedpyright
```

### JavaScript/TypeScript Projects

```bash
# Install dependencies
bun install

# Run script
bun run <script_name>

# Testing
bun test <test_file>
bun test --test-name-pattern "<test_name>"

# Code quality
bun run lint  # or eslint .
bun run format  # or prettier --write .

# Type checking
tsc --noEmit
```

## Project Structure

```
opencode-customizations/
├── pyproject.toml           # Project configuration (pytest, coverage, ruff, etc.)
├── AGENTS.md                # This file - development guidelines
├── README.md                # Project documentation
├── skills/                  # Skill packages
│   └── <skill-name>/        # Individual skill directory
│       ├── SKILL.md         # Skill documentation (with YAML frontmatter)
│       └── scripts/         # Python scripts for the skill
│           ├── <script>.py  # Main utility scripts
│           └── test_*.py    # Unit tests
└── evals/                   # Evaluation framework
    ├── test_<skill>_eval.py # Eval scripts
    └── test_data/           # Test data fixtures
        └── test_cases.json  # Test case definitions
```

## Code Style Guidelines

Python project settings (pytest, coverage, ruff, basedpyright, etc.) must be defined in `pyproject.toml`, not in separate configuration files like `.coveragerc`, `.pytest.ini`, or `pylintrc`.

### Python

#### Imports
- Standard library first: `import os, sys, json, re`
- Third-party imports with try/except:
  ```python
  try:
      import requests
  except ImportError:
      print("Error: requests module not found. Install with: uv add requests")
      sys.exit(1)
  ```
- Avoid star imports (`import *`)

#### Formatting
- 4-space indentation, 88 char line limit (Black)
- f-strings for formatting: `f"Error: {e}"`
- Shebang: `#!/usr/bin/env python3`

#### Functions & Classes
- snake_case functions, PascalCase classes, UPPER_SNAKE_CASE constants
- Docstrings required for all functions
- Keep functions focused and under 30 lines

#### Error Handling
- Specific exceptions (ValueError, KeyError) with helpful messages:
  ```python
  raise ValueError(f"Could not extract video ID from URL: {url}")
  ```
- Wrap external API calls in try/except
- Use `sys.exit(1)` for fatal errors in main functions

#### Environment Variables
- Uppercase: `YOUTUBE_API_KEY`, `VAULT_PATH`
- Check missing vars with clear error messages:
  ```python
  api_key = os.environ.get("YOUTUBE_API_KEY")
  if not api_key:
      print("Error: YOUTUBE_API_KEY environment variable not set")
      sys.exit(1)
  ```

#### File Operations
- Use `with open()` context manager with encoding="utf-8":
  ```python
  with open(output_path, "w", encoding="utf-8") as f:
      f.write(content)
  ```

#### Type Hints
- Add type hints for new code:
  ```python
  def extract_video_id(url: str) -> str:
      """Extract YouTube video ID from various URL formats."""
  ```

### JavaScript/TypeScript

#### Imports
- Use ES6 import syntax: `import { function } from 'module'`
- Group imports: standard lib → third-party → relative

#### Formatting
- 2-space indentation
- Use template literals: `` `Error: ${message}` ``
- Prefer const over let, avoid var

#### Naming
- Functions/variables: camelCase (`extractVideoId`)
- Classes: PascalCase (`VideoProcessor`)
- Constants: UPPER_SNAKE_CASE (`MAX_TAGS = 15`)

#### Error Handling
- Use async/await with try/catch
- Provide meaningful error messages
- Avoid silent failures

## Adding New Skills

1. **Create skill directory**:
   ```bash
   mkdir -p skills/<skill-name>/scripts
   ```

2. **Add skill documentation** (`skills/<skill-name>/SKILL.md`):
   ```yaml
   ---
   name: skill-name
   description: "Brief description of what the skill does"
   ---
   ```

3. **Create scripts** in `skills/<skill-name>/scripts/`:
   - Main utility scripts
   - Unit tests (`test_*.py`)

4. **Document prerequisites** in SKILL.md:
   - Environment variables required
   - External API keys
   - Installation instructions

5. **Use `uv`** for dependency management in pyproject.toml

## Dependencies

- **Python**: Use `uv` for package management (https://docs.astral.sh/uv/llms.txt)
- **JavaScript**: Use `bun` for package management (https://bun.sh/llms-full.txt)
- Add dependencies to pyproject.toml or package.json using `uv` or `bun`

## Testing

### Unit Tests
- Write tests for new features using pytest (Python) or bun test (JS/TS)
- Test file names: `test_*.py` or `*_test.py`
- Keep tests independent and focused
- Use descriptive test names
- **Coverage requirement**: 80%+ threshold

### Evaluation Tests
- Eval scripts in `evals/` directory test end-to-end functionality
- Test cases defined in `evals/test_data/test_cases.json`
- **Accuracy requirement**: 90%+ threshold for eval tests

### Skill-Specific Commands

#### youtube-obsidian

**Unit Tests**:
```bash
# Run all tests
uv run pytest skills/youtube-obsidian/scripts/test_yt.py -v

# Run with coverage
uv run pytest skills/youtube-obsidian/scripts/test_yt.py --cov=skills/youtube-obsidian/scripts --cov-report=html

# Run specific test class
uv run pytest skills/youtube-obsidian/scripts/test_yt.py::TestFetchTranscript -v
```

**Evaluation Tests**:
```bash
# Run eval script
uv run evals/test_youtube_obsidian_eval.py --video-url <URL>

# Run with verbose logging
uv run evals/test_youtube_obsidian_eval.py --video-url <URL> --verbose

# Custom vault path
uv run evals/test_youtube_obsidian_eval.py --video-url <URL> --vault-path ./output/
```

**Linting & Formatting**:
```bash
# Lint
uv run ruff check skills/youtube-obsidian/scripts/

# Format
uv run ruff format skills/youtube-obsidian/scripts/
```

**Capture Test Data** (requires YOUTUBE_API_KEY):
```bash
export YOUTUBE_API_KEY="your-api-key"
uv run scripts/capture_test_data.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

## Task Tracking

- Use issue tracking for task management during development
- Create new git branches for each feature/fix
- Write tests first, then implement the task
- Ensure all tests pass
- **Coverage must be over 80%** for unit tests
- **Accuracy score must be over 90%** for eval tests

### Implementing Issues
1. View open issues: Check your project's issue tracker
2. Understand requirements from issue details
3. Create a new git branch for the work
4. Implement following issue requirements
5. Update issue status when complete

## Configuration

All Python project configuration must be defined in `pyproject.toml`:

```toml
[tool.ruff]
line-length = 88
target-version = "py311"

[tool.pytest.ini_options]
testpaths = ["skills"]
addopts = "--cov=scripts --cov-report=term-missing --cov-report=html"

[tool.coverage.run]
omit = ["test_*.py"]
```

**Do NOT use**: `.coveragerc`, `.pytest.ini`, `pylintrc`, or similar separate config files.

## Security

- Never commit API keys, secrets, or credentials
- Use environment variables for sensitive data
- Validate user input before processing
- Use parameterized queries for database operations
- Add sensitive paths to `.gitignore`

## Git Workflow

- Use conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`
- Create descriptive commit messages
- Keep commits atomic and focused
- Use branch names that describe the feature/fix
- Never force push to main/master

## Example Commit Messages

```bash
feat(youtube-obsidian): add video transcript download functionality
fix(yt): handle missing YouTube API key gracefully
docs(agents): update testing guidelines
refactor(get_youtube_data): extract tag generation to separate function
test(youtube-obsidian): add unit tests for transcript fetching
chore(deps): update youtube-transcript-api to v0.6.0
```

## Common Patterns

### CLI Scripts with Typer
```python
import typer

app = typer.Typer()

@app.command()
def main(arg: str, option: str = typer.Option(default="value")):
    """Command description."""
    pass

if __name__ == "__main__":
    app()
```

### Error Handling with Environment Variables
```python
import os
import sys

def main():
    api_key = os.environ.get("API_KEY")
    if not api_key:
        print("Error: API_KEY environment variable not set")
        sys.exit(1)
```

### Testing with Mocks
```python
from unittest.mock import patch, MagicMock

@patch("module.external_function")
def test_function(mock_external):
    mock_external.return_value = "test"
    result = function_under_test()
    assert result == "expected"
```

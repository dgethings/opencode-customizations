# Development Guide

## Overview

This guide provides complete development setup and workflow instructions for opencode-customizations.

## Prerequisites

### Required Software

- **Python**: 3.11 or higher
- **Bun**: Latest version (for JavaScript/TypeScript)
- **uv**: Latest version (Python package manager)
- **Git**: For version control

### Optional Software

- **basedpyright**: Static type checking for Python
- **GitHub CLI** (gh): For GitHub operations

## Environment Setup

### Clone Repository

```bash
git clone <repository-url>
cd opencode-customizations
```

### Python Environment Setup

```bash
# Create virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install project dependencies with test dependencies
uv pip install -e ".[test]"
```

### JavaScript/TypeScript Environment Setup

```bash
# Install JavaScript/TypeScript dependencies
bun install
```

### Environment Variables

**For YouTube to Obsidian Skill:**

```bash
# Set YouTube API key
export YOUTUBE_API_KEY="your-youtube-data-api-v3-key"

# Set Obsidian vault path
export VAULT_PATH="/path/to/your/obsidian/vault"
```

**Getting YouTube API Key:**

1. Go to https://console.cloud.google.com/
2. Create a new project
3. Enable YouTube Data API v3
4. Create API key in Credentials section
5. Copy the API key

## Development Commands

### Python Development

**Install dependencies:**

```bash
# Add new dependency
uv add <package-name>

# Install from pyproject.toml
uv pip install -e ".[test]"
```

**Run scripts:**

```bash
# Run main script
uv run scripts/<script_name>.py <args>

# Example: YouTube to Obsidian
uv run skills/youtube-obsidian/scripts/get_youtube_data.py \
  "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  "My summary" \
  "My notes"
```

**Run tests:**

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest skills/youtube-obsidian/scripts/test_get_youtube_data.py -v

# Run specific test
uv run pytest skills/youtube-obsidian/scripts/test_get_youtube_data.py::TestExtractVideoId -v

# Run with pattern matching
uv run pytest -k "test_extract_video_id"
```

**Run with coverage:**

```bash
# Coverage with terminal output
uv run pytest --cov=skills/youtube-obsidian/scripts --cov-report=term-missing

# Coverage with HTML report
uv run pytest --cov=skills/youtube-obsidian/scripts --cov-report=html

# Open coverage report
open htmlcov/index.html  # On Windows: start htmlcov/index.html
```

**Code quality:**

```bash
# Lint code
uv run ruff check .

# Format code
uv run ruff format .

# Type check
basedpyright
```

### JavaScript/TypeScript Development

**Install dependencies:**

```bash
bun install
```

**Run tests:**

```bash
bun test
```

**Type check:**

```bash
tsc --noEmit
```

## Development Workflow

### Creating a New Skill

1. **Create skill directory:**

```bash
mkdir skills/<skill-name>
cd skills/<skill-name>
```

2. **Create skill structure:**

```bash
mkdir scripts
mkdir test_data
touch SKILL.md
```

3. **Add SKILL.md with frontmatter:**

```markdown
---
name: skill-name
description: "Brief description of what the skill does"
---

# Skill Name

## Description

Detailed description of the skill.

## Prerequisites

Required setup and dependencies.

## Usage

How to use the skill.

## Testing

Testing instructions.
```

4. **Implement scripts:**

```bash
# Create main script
scripts/main.py

# Create test file
scripts/test_main.py

# Create pytest config
touch conftest.py
```

5. **Add dependencies:**

```bash
cd ../../  # Back to project root
uv add <package-name>
```

6. **Write tests:**

```bash
# Run tests
uv run pytest skills/<skill-name>/scripts/test_main.py -v

# Ensure 80%+ coverage
uv run pytest skills/<skill-name>/scripts/test_main.py --cov=skills/<skill-name>/scripts --cov-fail-under=80
```

7. **Lint and format:**

```bash
uv run ruff check skills/<skill-name>/scripts/
uv run ruff format skills/<skill-name>/scripts/
```

### Testing Workflow

1. **Write tests first** (TDD approach)
2. **Run tests** to ensure they fail
3. **Implement code** to make tests pass
4. **Run tests** to verify passing
5. **Check coverage** to ensure 80%+ threshold
6. **Lint and format** code
7. **Type check** (if applicable)

### Running Evaluations

```bash
# Run evaluation script
uv run evals/eval_youtube_obsidian.py

# Capture test data (requires YOUTUBE_API_KEY)
export YOUTUBE_API_KEY="your-api-key"
uv run scripts/capture_test_data.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Task Tracking with Beads

```bash
# Show ready issues
bd ready

# List all issues
bd list --all

# Show issue details
bd show <issue-id>

# Create new branch for task
git checkout -b feature/<task-name>

# Close issue when complete
bd close <issue-id>
```

## Code Style Guidelines

### Python

**Imports:**
```python
# Standard library first
import os, sys, json, re

# Third-party imports with try/except
try:
    import requests
except ImportError:
    print("Error: requests module not found. Install with: uv add requests")
    sys.exit(1)
```

**Formatting:**
- 4-space indentation
- 88 character line limit
- f-strings for formatting
- Docstrings required for functions and classes

**Naming:**
- Functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`

**Error Handling:**
```python
# Check environment variables
api_key = os.environ.get("YOUTUBE_API_KEY")
if not api_key:
    print("Error: YOUTUBE_API_KEY environment variable not set")
    sys.exit(1)

# Handle external API calls
try:
    response = requests.get(url)
except requests.RequestException as e:
    print(f"Error fetching data: {e}")
    sys.exit(1)
```

**File Operations:**
```python
# Always use context manager with encoding
with open(output_path, "w", encoding="utf-8") as f:
    f.write(content)
```

### TypeScript

**Formatting:**
- 2-space indentation
- ES6 import syntax
- Template literals for strings
- const over let, avoid var

**Naming:**
- Functions/variables: `camelCase`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`

**Error Handling:**
```typescript
try {
  const result = await fetchData(url);
} catch (error) {
  console.error(`Error: ${error.message}`);
  throw error;
}
```

## Git Workflow

### Branch Naming

- Feature: `feature/<feature-name>`
- Bugfix: `fix/<bug-description>`
- Chore: `chore/<task-description>`

### Commit Messages

Use conventional commits:

```
feat: add new skill for processing data
fix: correct API authentication issue
docs: update README with new instructions
refactor: simplify data processing logic
test: add unit tests for extraction function
chore: update dependencies
```

### Commit Process

```bash
# Stage changes
git add .

# Commit with conventional message
git commit -m "feat: add new skill"

# Push to remote
git push origin feature/new-skill
```

### Pull Request Process

1. Create pull request from feature branch to main/develop
2. Ensure CI/CD checks pass
3. Request code review
4. Address review feedback
5. Merge after approval

## Common Development Tasks

### Adding a Dependency

```bash
# Python
uv add <package-name>

# JavaScript/TypeScript
bun add <package-name>
```

### Running Specific Tests

```bash
# Run all tests for youtube-obsidian skill
uv run pytest skills/youtube-obsidian/scripts/test_get_youtube_data.py -v

# Run specific test class
uv run pytest skills/youtube-obsidian/scripts/test_get_youtube_data.py::TestExtractVideoId -v

# Run specific test method
uv run pytest skills/youtube-obsidian/scripts/test_get_youtube_data.py::TestExtractVideoId::test_standard_url -v

# Run tests matching pattern
uv run pytest -k "extract_video_id"
```

### Checking Coverage

```bash
# Coverage with threshold check
uv run pytest --cov=skills/youtube-obsidian/scripts --cov-fail-under=80

# Coverage with HTML report
uv run pytest --cov=skills/youtube-obsidian/scripts --cov-report=html
open htmlcov/index.html
```

### Linting and Formatting

```bash
# Check for linting issues
uv run ruff check .

# Auto-fix linting issues
uv run ruff check --fix .

# Format code
uv run ruff format .

# Check format without modifying
uv run ruff format --check .
```

### Type Checking

```bash
# Run basedpyright
basedpyright

# Or use tsc for TypeScript
tsc --noEmit
```

## Debugging

### Python Debugging

```bash
# Run with pdb (Python debugger)
uv run python -m pdb scripts/<script_name>.py

# Use print statements (quick debugging)
print(f"Debug: variable = {variable}")

# Use logging module (recommended)
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug(f"Debug: variable = {variable}")
```

### Testing with Verbose Output

```bash
# Verbose pytest output
uv run pytest -v -s

# Show print statements
uv run pytest -s
```

## Troubleshooting

### Common Issues

**Import errors:**
```bash
# Install dependencies
uv pip install -e ".[test]"

# Check virtual environment is activated
which python  # Should show .venv/bin/python
```

**Coverage below 80%:**
```bash
# Check what's not covered
uv run pytest --cov=skills/youtube-obsidian/scripts --cov-report=term-missing

# Add tests for uncovered lines
```

**Linting errors:**
```bash
# Auto-fix most issues
uv run ruff check --fix .

# Format code
uv run ruff format .
```

**Type checking errors:**
```bash
# Check type errors
basedpyright

# Add type hints to fix errors
def my_function(param: str) -> str:
    return param
```

## Resources

- **uv documentation**: https://docs.astral.sh/uv/
- **Bun documentation**: https://bun.sh/
- **pytest documentation**: https://docs.pytest.org/
- **ruff documentation**: https://docs.astral.sh/ruff/
- **basedpyright documentation**: https://github.com/detachhead/basedpyright
- **YouTube Data API**: https://developers.google.com/youtube/v3

## Best Practices

1. **Write tests first** (TDD)
2. **Keep functions focused** and under 30 lines
3. **Use descriptive names** for functions, variables, and tests
4. **Add docstrings** to all functions and classes
5. **Maintain 80%+ coverage** threshold
6. **Run linting and formatting** before committing
7. **Use environment variables** for sensitive data
8. **Never commit API keys** or secrets
9. **Write clear commit messages** using conventional commits
10. **Create feature branches** for all work

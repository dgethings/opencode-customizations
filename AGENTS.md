# Opencode Customizations - Agent Guidelines

## Project Overview
This repository contains customizations for Opencode (https://opencode.ai/). It's a collection of skills and utilities for automating workflows.

## Build, Lint, Test Commands

### Python Projects (Primary)
- **Install dependencies**: `uv pip install -r requirements.txt` (if requirements.txt exists) or `uv add <package>` - prefer to use `uv add <package>`
- **Run script**: `uv run scripts/<script_name>.py <args>`
- **Single test**: `uv run pytest tests/<test_file>.py::<test_function>` or `uv run pytest -k "<test_name>"` (if tests exist)
- **All tests**: `uv run pytest`
- **Lint**: `uv run ruff check .` (add ruff configuration to pyproject.toml)
- **Format**: `uv run ruff format .`
- **Type check**: `basedpyright` (add type annotations first)

### JavaScript/TypeScript Projects
- **Install dependencies**: `bun install`
- **Run script**: `bun run <script_name>`
- **Single test**: `bun test <test_file>` or `bun test --test-name-pattern "<test_name>"`
- **All tests**: `bun test`
- **Lint**: `bun run lint` (if configured) or `eslint .`
- **Format**: `bun run format` (if configured) or `prettier --write .`
- **Type check**: `tsc --noEmit`

## Code Style Guidelines

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
- Docstrings required
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
- Add type hints for new code (not enforced in existing):
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

## Project Structure
- `skills/`: Skill packages for Opencode
  - Each skill has a `SKILL.md` documentation file
  - `scripts/` directory for executable scripts
- `evals/`: Evaluation files (if applicable)

## Adding New Skills
1. Create directory in `skills/<skill-name>/`
2. Add `SKILL.md` with YAML frontmatter:
   ```yaml
   ---
   name: skill-name
   description: "Brief description of what the skill does"
   ---
   ```
3. Create `scripts/` directory for Python scripts
4. Document prerequisites and environment variables
5. Use `uv` for dependency management

## Dependencies
- Python: Use `uv` for package management (https://docs.astral.sh/uv/llms.txt)
- JavaScript: Use `bun` for package management (https://bun.sh/llms-full.txt)
- Add dependencies to pyproject.toml or package.json using `uv` or `bun`

## Task Tracking
- Use 'bd' for task tracking during development

## Testing
- Write tests for new features using pytest (Python) or bun test (JS/TS)
- Test file names: `test_*.py` or `*_test.py`
- Keep tests independent and focused
- Use descriptive test names

## Security
- Never commit API keys, secrets, or credentials
- Use environment variables for sensitive data
- Validate user input before processing
- Use parameterized queries for database operations

## Git Workflow
- Create descriptive commit messages
- Keep commits atomic and focused
- Use branch names that describe the feature/fix
- Never force push to main/master

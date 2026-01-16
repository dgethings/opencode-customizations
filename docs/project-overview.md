# Project Overview

## Project Name

**opencode-customizations**

## Purpose

A collection of customizations and skill packages for [Opencode AI](https://opencode.ai/), enabling automation workflows and integrations.

## Executive Summary

opencode-customizations is a library repository that provides reusable skill packages extending Opencode AI capabilities. The project follows a modular architecture where each skill is self-contained with its own implementation, tests, and documentation. Skills are discovered and loaded dynamically by Opencode AI, making it easy to add new functionality without modifying core systems.

**Key Highlights:**

- ✅ **Modular Architecture:** Self-contained skill packages
- ✅ **Dual-Language Support:** Python 3.11+ and TypeScript 5+
- ✅ **Comprehensive Testing:** 80%+ coverage threshold
- ✅ **Quality Gates:** Automated linting, formatting, type checking
- ✅ **Documentation-First:** Complete SKILL.md for every skill
- ✅ **BMAD Integration:** Internal methodology framework for structured development

## Tech Stack Summary

| Category | Technology | Version |
|----------|-----------|----------|
| **Primary Language** | Python | 3.11+ |
| **Secondary Language** | TypeScript | 5+ |
| **JavaScript Runtime** | Bun | latest |
| **Python Package Manager** | uv | latest |
| **Python Build System** | setuptools | 68.0+ |
| **Testing Framework** | pytest | 8.0+ |
| **Code Quality** | ruff | latest |
| **Type Checker** | basedpyright | latest |

## Architecture Type Classification

**Repository Structure:** Monolith (single cohesive codebase)

**Architecture Pattern:** Modular Skill Package Repository

**Parts:** 1 part (opencode-customizations)

**Description:**
- Library repository with self-contained skill packages
- Skills are discovered and loaded dynamically by Opencode AI
- Internal BMAD framework for structured development
- No traditional application entry points

## Repository Structure

```
opencode-customizations/
├── skills/                    # Skill packages
│   └── youtube-obsidian/     # YouTube to Obsidian skill
│       ├── scripts/              # Python implementation
│       ├── test_data/            # Test fixtures
│       └── SKILL.md             # Skill documentation
├── _bmad/                      # BMAD framework (internal)
│   ├── core/                    # Core workflow engine
│   ├── bmm/                     # BMAD methodology
│   └── bmb/                     # Builder tools
├── _bmad-output/               # Generated artifacts
│   ├── planning-artifacts/        # PRD, architecture, epics
│   └── implementation-artifacts/ # Implementation docs
├── scripts/                     # Utility scripts
├── evals/                       # Evaluation scripts
├── docs/                        # Generated documentation
│   ├── index.md                  # Master index (this file)
│   ├── project-overview.md       # Overview (this file)
│   ├── architecture.md           # Architecture
│   ├── development-guide.md      # Development guide
│   ├── deployment-guide.md       # CI/CD and deployment
│   └── ...                      # More documentation
├── AGENTS.md                    # Agent guidelines
├── README.md                    # Project readme
├── pyproject.toml               # Python config
├── package.json                 # JavaScript config
└── .github/workflows/test.yml   # CI/CD workflow
```

## Key Components

### 1. Skill Packages (skills/)

**Purpose:** Provide reusable functionality for Opencode AI

**Current Skills:**

**youtube-obsidian**
- Extract YouTube video metadata and transcripts
- Create structured Obsidian markdown notes with frontmatter
- Auto-generate relevant tags from content
- API integration: YouTube Data API v3, youtube-transcript-api

**Future Skills:**
- Placeholder for additional skills

### 2. BMAD Framework (_bmad/)

**Purpose:** Internal methodology for structured development

**Components:**
- **core/**: Workflow execution engine
- **bmm/**: BMAD methodology workflows (document-project, create-prd, etc.)
- **bmb/**: Builder tools for agents and workflows

**Note:** Not part of public API - used internally for development methodology

### 3. Development Infrastructure

**scripts/**: Utility scripts for development and testing
- capture_test_data.py - Capture real API data for testing

**evals/**: Evaluation scripts for skill validation
- eval_youtube_obsidian.py - Evaluates skill performance (>90% accuracy required)

**.github/workflows/**: CI/CD automation
- test.yml - Automated testing, linting, formatting, coverage

## Links to Detailed Documentation

### Project Documentation

- [Project Structure](./project-structure.md) - Directory structure overview
- [Project Parts Metadata](./project-parts-metadata.md) - Parts breakdown
- [Source Tree Analysis](./source-tree-analysis.md) - Annotated directory tree
- [Critical Folders Summary](./critical-folders-summary.md) - Critical directories

### Technical Documentation

- [Technology Stack](./technology-stack.md) - Complete technology table
- [Architecture Patterns](./architecture-patterns.md) - Architecture patterns
- [Architecture](./architecture.md) - Detailed architecture documentation
- [Comprehensive Analysis](./comprehensive-analysis.md) - Pattern analysis

### Development Documentation

- [Development Guide](./development-guide.md) - Complete development workflow
- [Deployment Guide](./deployment-guide.md) - CI/CD and deployment processes
- [Contribution Guide](./contribution-guide.md) - Contribution guidelines

### Inventory and Context

- [Existing Documentation Inventory](./existing-documentation-inventory.md) - Existing docs found
- [User Provided Context](./user-provided-context.md) - User context

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Bun (for JavaScript/TypeScript)
- uv (Python package manager)
- Git

### Quick Start

1. **Clone repository:**

```bash
git clone <repository-url>
cd opencode-customizations
```

2. **Setup Python environment:**

```bash
python3 -m venv .venv
source .venv/bin/activate
curl -LsSf https://astral.sh/uv/install.sh | sh
uv pip install -e ".[test]"
```

3. **Setup JavaScript environment:**

```bash
bun install
```

4. **Set environment variables (for youtube-obsidian):**

```bash
export YOUTUBE_API_KEY="your-youtube-data-api-v3-key"
export VAULT_PATH="/path/to/your/obsidian/vault"
```

5. **Run YouTube to Obsidian skill:**

```bash
uv run skills/youtube-obsidian/scripts/get_youtube_data.py \
  "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  "My summary" \
  "My notes"
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=skills/youtube-obsidian/scripts --cov-report=html

# Run specific skill tests
uv run pytest skills/youtube-obsidian/scripts/test_get_youtube_data.py -v
```

### Code Quality

```bash
# Lint code
uv run ruff check .

# Format code
uv run ruff format .

# Type check
basedpyright
```

## Current Status

**Version:** 0.1.0

**Skills:** 1 (youtube-obsidian)

**Test Coverage:** 91.30% (youtube-obsidian skill)

**CI/CD:** ✅ GitHub Actions configured and passing

## Project Type Detection

**Detected Type:** library

**Key Indicators:**
- `pyproject.toml` with setuptools packaging
- `package.json` with TypeScript configuration
- `skills/` directory containing skill packages
- `_bmad/` internal framework directory
- No traditional application entry points

## Development Status

**Active Development:** ✅ Yes

**Last Updated:** 2026-01-14

**Next Milestones:**
- Add more skill packages
- Improve test coverage to >95%
- Add automated skill validation
- Expand documentation

## Contact and Support

- **Repository:** https://github.com/<username>/opencode-customizations
- **Documentation:** This `docs/` directory
- **Issues:** GitHub Issues (if enabled)
- **Discussions:** GitHub Discussions (if enabled)

## License

See LICENSE file for details.

## Summary

| Aspect | Details |
|---------|---------|
| **Name** | opencode-customizations |
| **Purpose** | Opencode AI customizations and skill packages |
| **Type** | Library/repository |
| **Architecture** | Modular skill packages |
| **Languages** | Python 3.11+, TypeScript 5+ |
| **Skills** | 1 (youtube-obsidian) |
| **Test Coverage** | 91.30% (current skill) |
| **CI/CD** | GitHub Actions |
| **Documentation** | Complete (SKILL.md + project docs) |

For detailed information, explore the documentation links above.

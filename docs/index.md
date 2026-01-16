# Project Documentation Index

## Project Overview

- **Type:** Monolith (single cohesive codebase)
- **Primary Language:** Python 3.11+
- **Secondary Language:** TypeScript 5+
- **Architecture:** Modular Skill Package Repository

## Quick Reference

- **Tech Stack:** Python 3.11+, TypeScript 5+, Bun, uv, pytest, ruff
- **Entry Points:** Skill-specific (no global entry point)
- **Architecture Pattern:** Library/Package Repository with self-contained skill packages
- **Parts Count:** 1 (opencode-customizations)

## Generated Documentation

### Project Documentation

- [Project Overview](./project-overview.md) - Executive summary, quick start, and getting started guide
- [Project Structure](./project-structure.md) - Repository overview with directory structure
- [Project Parts Metadata](./project-parts-metadata.md) - Parts breakdown and technology markers
- [Source Tree Analysis](./source-tree-analysis.md) - Complete annotated directory tree
- [Critical Folders Summary](./critical-folders-summary.md) - Summary of critical directories
- [Component Inventory](./component-inventory.md) - Complete component inventory by type

### Technical Documentation

- [Technology Stack](./technology-stack.md) - Complete technology table and dependencies
- [Architecture Patterns](./architecture-patterns.md) - Architecture patterns and principles
- [Architecture](./architecture.md) - Detailed system architecture documentation
- [Comprehensive Analysis](./comprehensive-analysis.md) - Pattern analysis and conditional requirements

### Development Documentation

- [Development Guide](./development-guide.md) - Complete development setup and workflow
- [Deployment Guide](./deployment-guide.md) - CI/CD configuration and deployment processes
- [Contribution Guide](./contribution-guide.md) - Contribution guidelines and code of conduct

### Inventory and Context

- [Existing Documentation Inventory](./existing-documentation-inventory.md) - Inventory of existing documentation files
- [User Provided Context](./user-provided-context.md) - User context notes

## Existing Documentation

- [README](../README.md) - Brief project overview and link to Opencode documentation
- [Agent Guidelines](../AGENTS.md) - Agent guidelines, build/test commands, and code style guidelines
- [YouTube to Obsidian SKILL](../skills/youtube-obsidian/SKILL.md) - Complete usage guide for youtube-obsidian skill
- [BMAD BMB README](../_bmad/bmb/README.md) - BMB (BMad Builder Module) overview

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Bun (for JavaScript/TypeScript)
- uv (Python package manager)
- Git

### Quick Setup

```bash
# Clone repository
git clone <repository-url>
cd opencode-customizations

# Setup Python environment
python3 -m venv .venv
source .venv/bin/activate
curl -LsSf https://astral.sh/uv/install.sh | sh
uv pip install -e ".[test]"

# Setup JavaScript environment
bun install

# Set environment variables (for youtube-obsidian skill)
export YOUTUBE_API_KEY="your-youtube-data-api-v3-key"
export VAULT_PATH="/path/to/your/obsidian/vault"
```

### Running YouTube to Obsidian Skill

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

## Key Components

### Skills Directory

Contains Opencode skill packages that extend AI capabilities.

**Current Skills:**
- **youtube-obsidian** - Extract YouTube video metadata and transcripts to create Obsidian markdown notes

**Skill Structure:**
```
skills/youtube-obsidian/
├── scripts/              # Python implementation
│   ├── get_youtube_data.py    # Main script
│   └── test_get_youtube_data.py # Tests (91.30% coverage)
├── test_data/            # Test fixtures
└── SKILL.md             # Complete usage guide
```

### BMAD Framework

Internal methodology framework for structured development.

**Components:**
- **core/** - Core workflow engine
- **bmm/** - BMAD methodology workflows
- **bmb/** - Builder tools

**Note:** Not part of public API - used internally for development methodology.

### Documentation Output

Generated documentation for AI-assisted development.

**Location:** `docs/` directory

**Purpose:** Primary AI retrieval source for brownfield PRD

## Quality Gates

All code must pass the following checks before merging:

- ✅ All tests pass (pytest)
- ✅ Coverage ≥ 80% (pytest-cov)
- ✅ No linting errors (ruff check)
- ✅ Code formatted (ruff format)
- ✅ Type checking passes (basedpyright)
- ✅ Evaluation passes (eval script)

## CI/CD

**Location:** `.github/workflows/test.yml`

**Triggers:** Push to main/develop, PR to main/develop

**Pipeline:**
1. Unit tests with mocked APIs
2. Coverage threshold check (80%)
3. Linting (ruff check)
4. Format check (ruff format)
5. Evaluation script
6. Coverage upload to Codecov
7. Integration tests (main branch only, real API)

## Documentation by Purpose

### For New Developers

Start with:
1. [Project Overview](./project-overview.md) - Understand the project
2. [Development Guide](./development-guide.md) - Setup development environment
3. [Contribution Guide](./contribution-guide.md) - Learn contribution guidelines

### For Understanding Architecture

Read:
1. [Architecture](./architecture.md) - Complete system architecture
2. [Architecture Patterns](./architecture-patterns.md) - Architecture patterns and principles
3. [Technology Stack](./technology-stack.md) - Technology stack and dependencies

### For Using Skills

Reference:
1. [YouTube to Obsidian SKILL](../skills/youtube-obsidian/SKILL.md) - Complete skill usage guide
2. [Project Overview](./project-overview.md) - Quick start guide

### For Understanding Project Structure

Explore:
1. [Project Structure](./project-structure.md) - Directory structure overview
2. [Source Tree Analysis](./source-tree-analysis.md) - Annotated directory tree
3. [Critical Folders Summary](./critical-folders-summary.md) - Critical directories
4. [Component Inventory](./component-inventory.md) - Complete component inventory

### For Deployment and Ops

Read:
1. [Deployment Guide](./deployment-guide.md) - CI/CD and deployment processes
2. [Comprehensive Analysis](./comprehensive-analysis.md) - Pattern analysis and configuration

### For Contributing

Follow:
1. [Contribution Guide](./contribution-guide.md) - Contribution guidelines
2. [Development Guide](./development-guide.md) - Development workflow
3. [Existing Documentation Inventory](./existing-documentation-inventory.md) - Understand existing docs

## Project Status

**Version:** 0.1.0

**Skills:** 1 (youtube-obsidian)

**Test Coverage:** 91.30% (youtube-obsidian skill)

**CI/CD:** ✅ GitHub Actions configured and passing

**Documentation:** ✅ Complete (SKILL.md + project docs)

## Contact and Support

- **Repository:** https://github.com/<username>/opencode-customizations
- **Documentation:** This `docs/` directory
- **Issues:** GitHub Issues (if enabled)
- **Discussions:** GitHub Discussions (if enabled)

## Summary

This index provides a comprehensive overview of all documentation for the opencode-customizations project. Use the links above to navigate to specific topics.

**Primary Documentation:**
- [Project Overview](./project-overview.md) - Executive summary and quick start
- [Architecture](./architecture.md) - System architecture
- [Development Guide](./development-guide.md) - Development workflow

**Key Skills:**
- [YouTube to Obsidian](../skills/youtube-obsidian/SKILL.md) - Extract YouTube content to Obsidian

**Quality Standards:**
- 80%+ test coverage (currently 91.30%)
- Automated linting and formatting
- Comprehensive documentation
- CI/CD validation on every push

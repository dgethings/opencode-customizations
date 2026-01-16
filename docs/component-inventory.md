# Component Inventory

## Overview

This document provides an inventory of all components in the opencode-customizations project, categorized by type and usage.

## Project Structure

**Repository:** Monolith (1 part)  
**Part:** opencode-customizations  
**Project Type:** library

## Component Categories

### 1. Skill Packages

**Location:** `skills/`

**Purpose:** Reusable functionality for Opencode AI

#### YouTube to Obsidian Skill

**Location:** `skills/youtube-obsidian/`

**Type:** Skill Package

**Description:** Extract YouTube video metadata and transcripts to create structured Obsidian markdown notes with frontmatter.

**Components:**

| Component | Type | Location | Purpose |
|-----------|-------|-----------|---------|
| **get_youtube_data.py** | Main Script | `scripts/` | Entry point for skill |
| **test_get_youtube_data.py** | Test Suite | `scripts/` | Comprehensive tests (30 tests, 91.30% coverage) |
| **test_helpers.py** | Test Helpers | `scripts/` | Test fixtures and utilities |
| **test_create_obsidian_note_expanded.py** | Test Module | `scripts/` | Note creation tests |
| **test_generate_tags_expanded.py** | Test Module | `scripts/` | Tag generation tests |
| **test_get_transcript_expanded.py** | Test Module | `scripts/` | Transcript handling tests |
| **test_get_video_metadata_expanded.py** | Test Module | `scripts/` | Metadata fetching tests |
| **conftest.py** | Test Config | `scripts/` | Pytest configuration |
| **SKILL.md** | Documentation | Root | Complete usage guide |
| **test_data/** | Test Fixtures | `test_data/` | Mocked API responses |

**Entry Point:** `scripts/get_youtube_data.py`

**External APIs:**
- YouTube Data API v3 (metadata)
- youtube-transcript-api (transcripts)

**Reusability:** High - Self-contained skill package

### 2. BMAD Framework (Internal)

**Location:** `_bmad/`

**Purpose:** Structured development methodology (internal use only)

#### Core Workflow Engine

**Location:** `_bmad/core/`

**Type:** Internal Framework

**Components:**

| Component | Type | Location | Purpose |
|-----------|-------|-----------|---------|
| **tasks/** | Task Definitions | `tasks/` | Workflow task execution |
| **workflows/** | Workflow Definitions | `workflows/` | Workflow orchestration |
| **agents/** | Agent Definitions | `agents/` | Agent management |
| **resources/** | Resources | `resources/` | Templates and configs |

**Reusability:** Internal - Not part of public API

#### BMAD Methodology

**Location:** `_bmad/bmm/`

**Type:** Internal Framework

**Components:**

| Component | Type | Location | Purpose |
|-----------|-------|-----------|---------|
| **workflows/** | Workflows | `workflows/` | Methodology workflows (document-project, create-prd, etc.) |
| **agents/** | Agents | `agents/` | Methodology agents |
| **data/** | Data | `data/` | CSV files, JSON configs |
| **teams/** | Team Definitions | `teams/` | Team configurations |
| **testarch/** | Test Architecture | `testarch/` | Test architecture workflows |

**Key Workflows:**
- document-project - Project documentation workflow
- create-prd - Product Requirements Document
- create-architecture - Architecture document
- create-epics-and-stories - Epics and stories breakdown
- implementation-readiness - Implementation readiness check

**Reusability:** Internal - Used by agents for structured development

#### BMAD Builder Module

**Location:** `_bmad/bmb/`

**Type:** Internal Framework

**Components:**

| Component | Type | Location | Purpose |
|-----------|-------|-----------|---------|
| **agents/** | Builder Agents | `agents/` | Agent creation tools |
| **workflows/** | Builder Workflows | `workflows/` | Builder workflow templates |

**Purpose:** Tools for creating, customizing, and extending BMad components

**Reusability:** Internal - Builder tools for framework development

### 3. Development Infrastructure

**Location:** Root directory

#### Utility Scripts

**Location:** `scripts/`

**Type:** Development Tools

**Components:**

| Component | Type | Purpose |
|-----------|-------|---------|
| **capture_test_data.py** | Utility Script | Capture real API data for youtube-obsidian testing |

**Reusability:** High - Reusable for future skills

#### Evaluation Scripts

**Location:** `evals/`

**Type:** Quality Assurance

**Components:**

| Component | Type | Purpose |
|-----------|-------|---------|
| **eval_youtube_obsidian.py** | Evaluation Script | Evaluates skill performance (>90% accuracy required) |
| **test_eval_youtube_obsidian.py** | Evaluation Tests | Tests for evaluation script |

**Reusability:** Medium - Can be adapted for other skills

### 4. CI/CD Pipeline

**Location:** `.github/workflows/`

**Type:** Automation

**Components:**

| Component | Type | Purpose |
|-----------|-------|---------|
| **test.yml** | GitHub Actions Workflow | Automated testing, linting, formatting, coverage |

**Pipeline Stages:**
1. Unit tests (mocked APIs)
2. Coverage threshold check (80%)
3. Linting (ruff check)
4. Format check (ruff format)
5. Evaluation script
6. Coverage upload to Codecov
7. Integration tests (main branch only, real API)

**Triggers:** Push to main/develop, PR to main/develop

**Reusability:** High - Configured for all skills

### 5. Documentation

**Location:** `docs/`

**Type:** Generated Documentation

**Components:**

| Component | Type | Purpose |
|-----------|-------|---------|
| **index.md** | Master Index | Primary AI retrieval source |
| **project-overview.md** | Overview | Executive summary and quick start |
| **architecture.md** | Architecture | Detailed system architecture |
| **technology-stack.md** | Tech Stack | Technology table and dependencies |
| **architecture-patterns.md** | Patterns | Architecture patterns and principles |
| **comprehensive-analysis.md** | Analysis | Pattern analysis and findings |
| **project-structure.md** | Structure | Directory structure overview |
| **project-parts-metadata.md** | Metadata | Parts breakdown |
| **source-tree-analysis.md** | Source Tree | Annotated directory tree |
| **critical-folders-summary.md** | Folders | Critical directories summary |
| **development-guide.md** | Guide | Complete development workflow |
| **deployment-guide.md** | Guide | CI/CD and deployment processes |
| **contribution-guide.md** | Guide | Contribution guidelines |
| **existing-documentation-inventory.md** | Inventory | Existing docs inventory |
| **user-provided-context.md** | Context | User context notes |
| **project-scan-report.json** | State | Workflow state file |

**Purpose:** Primary AI retrieval source for brownfield PRD

**Reusability:** High - Comprehensive project documentation

### 6. Existing Documentation

**Location:** Root directory

**Components:**

| Component | Type | Purpose |
|-----------|-------|---------|
| **README.md** | Project Readme | Brief project overview |
| **AGENTS.md** | Agent Guidelines | Development guidelines and workflow instructions |
| **skills/youtube-obsidian/SKILL.md** | Skill Documentation | Complete skill usage guide |
| **_bmad/bmb/README.md** | Framework Readme | BMB overview and links |

### 7. Configuration Files

**Location:** Root directory

**Components:**

| Component | Type | Purpose |
|-----------|-------|---------|
| **pyproject.toml** | Python Config | Python project configuration, dependencies, testing |
| **package.json** | JavaScript Config | JavaScript/TypeScript dependencies |
| **tsconfig.json** | TypeScript Config | TypeScript compiler configuration |
| **bun.lock** | Lockfile | Bun dependency lockfile |
| **uv.lock** | Lockfile | uv dependency lockfile |

### 8. Generated Artifacts

**Location:** `_bmad-output/`

**Components:**

| Component | Type | Purpose |
|-----------|-------|---------|
| **planning-artifacts/prd.md** | PRD | Product Requirements Document |
| **planning-artifacts/architecture.md** | Architecture | Architecture document |
| **planning-artifacts/epics.md** | Epics | Epics and stories breakdown |
| **planning-artifacts/bmm-workflow-status.yaml** | Status | BMAD workflow status tracking |
| **implementation-artifacts/** | Implementation | Implementation documentation |

**Generated by:** BMAD workflows

**Purpose:** Planning and implementation artifacts

## Component Classification

### By Type

| Type | Count | Examples |
|-------|--------|-----------|
| **Skill Packages** | 1 | youtube-obsidian |
| **Internal Framework** | 1 | BMAD (core, bmm, bmb) |
| **Utility Scripts** | 1 | capture_test_data.py |
| **Evaluation Scripts** | 1 | eval_youtube_obsidian.py |
| **CI/CD Workflows** | 1 | test.yml |
| **Documentation Files** | 15 | Generated docs + existing docs |
| **Configuration Files** | 5 | pyproject.toml, package.json, etc. |

### By Reusability

| Reusability | Components |
|--------------|-------------|
| **High** | Skill packages, CI/CD, documentation |
| **Medium** | Evaluation scripts, utility scripts |
| **Low** | Internal framework (BMAD) |
| **Single-Use** | Specific test fixtures |

### By Criticality

| Criticality | Components |
|-------------|-------------|
| **Critical** | Skills (youtube-obsidian), docs (index.md) |
| **Important** | BMAD framework (internal), CI/CD |
| **Useful** | Utility scripts, evaluation scripts |

## Component Dependencies

### YouTube to Obsidian Skill Dependencies

**Python Dependencies:**
- `requests >= 2.31.0` - HTTP client
- `youtube-transcript-api >= 0.6.0` - Transcript extraction

**External APIs:**
- YouTube Data API v3
- youtube-transcript-api

**Environment Variables:**
- `YOUTUBE_API_KEY`
- `VAULT_PATH`

### Development Infrastructure Dependencies

**Testing:**
- pytest 8.0+
- pytest-mock 3.12+
- pytest-cov 4.0+
- requests-mock 1.12+

**Code Quality:**
- ruff (latest)
- basedpyright (latest)

**Package Management:**
- uv (Python)
- bun (JavaScript/TypeScript)

## Component Relationships

```
Opencode AI (External)
    ↓ (uses)
skills/youtube-obsidian/ (Skill)
    ↓ (developed using)
_bmad/ (BMAD Framework)
    ↓ (generates)
docs/ (Documentation)
    ↓ (validated by)
.github/workflows/test.yml (CI/CD)
    ↓ (tested with)
scripts/ and evals/ (Infrastructure)
```

## Future Components

### Potential Additions

**Additional Skills:**
- [ ] Skill for processing PDFs
- [ ] Skill for web scraping
- [ ] Skill for data visualization
- [ ] Skill for API integration

**Infrastructure Enhancements:**
- [ ] Automated skill validation workflow
- [ ] Skill registry for better discoverability
- [ ] Skill versioning system
- [ ] Performance monitoring dashboard

## Component Maintenance

### Regular Updates

**Dependencies:**
- Monthly review of Python and JavaScript dependencies
- Security updates via GitHub Dependabot (if enabled)
- Update uv and Bun regularly

**Documentation:**
- Keep SKILL.md updated with new features
- Update project docs on major changes
- Update AGENTS.md with new guidelines

**Testing:**
- Maintain 80%+ coverage threshold
- Add tests for new features
- Update test fixtures as needed

## Summary

| Category | Count | Key Components |
|----------|--------|----------------|
| **Skill Packages** | 1 | youtube-obsidian |
| **Internal Framework** | 3 parts | core, bmm, bmb |
| **Infrastructure** | 2 | scripts, evals |
| **CI/CD** | 1 | test.yml |
| **Documentation** | 15 | Generated + existing |
| **Configuration** | 5 | Python, JS, TS configs |

**Total Components:** ~40 components across 8 categories

**Most Critical:** Skills (youtube-obsidian), Documentation (index.md), CI/CD (test.yml)

**Highest Reusability:** Skill packages, documentation, CI/CD pipeline

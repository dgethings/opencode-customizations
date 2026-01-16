# Source Tree Analysis

## Project Root Structure

```
opencode-customizations/
├── _bmad/                          # BMAD Framework (internal methodology)
│   ├── _config/                     # BMAD configuration
│   │   ├── agents/                  # Agent configurations
│   │   └── custom/                 # Custom BMAD settings
│   ├── bmb/                        # BMAD Builder Module
│   │   ├── agents/                  # Builder agent definitions
│   │   └── workflows/               # Builder workflow templates
│   ├── bmm/                        # BMAD Methodology
│   │   ├── agents/                  # Methodology agents
│   │   ├── data/                    # Data files (CSV, JSON)
│   │   ├── teams/                   # Team definitions
│   │   ├── testarch/                # Test architecture workflows
│   │   └── workflows/               # Methodology workflows
│   │       ├── document-project/     # Documentation workflow
│   │       └── [other workflows]
│   └── core/                       # Core workflow engine
│       ├── agents/                  # Core agents
│       ├── resources/               # Resources and templates
│       ├── tasks/                   # Task definitions
│       └── workflows/               # Core workflows
│
├── _bmad-output/                   # Generated BMAD artifacts
│   ├── implementation-artifacts/     # Implementation outputs
│   └── planning-artifacts/          # Planning outputs (PRD, architecture, epics)
│       ├── prd.md                   # Product Requirements Document
│       ├── architecture.md           # Architecture document
│       ├── epics.md                 # Epics and stories
│       └── bmm-workflow-status.yaml  # Workflow status tracking
│
├── skills/                         # Skill packages for Opencode AI
│   └── youtube-obsidian/           # YouTube to Obsidian skill
│       ├── scripts/                 # Python implementation
│       │   ├── get_youtube_data.py      # Main script (entry point)
│       │   ├── test_get_youtube_data.py  # Test suite (30 tests, 91.30% coverage)
│       │   ├── test_helpers.py           # Test helpers and fixtures
│       │   ├── test_create_obsidian_note_expanded.py
│       │   ├── test_generate_tags_expanded.py
│       │   ├── test_get_transcript_expanded.py
│       │   ├── test_get_video_metadata_expanded.py
│       │   └── conftest.py             # Pytest configuration
│       ├── test_data/                # Test fixtures
│       └── SKILL.md                  # Skill documentation (complete usage guide)
│
├── scripts/                        # Root-level utility scripts
│   └── capture_test_data.py         # Test data capture for youtube-obsidian
│
├── evals/                          # Evaluation scripts
│   ├── eval_youtube_obsidian.py      # Main evaluation script
│   └── test_eval_youtube_obsidian.py # Evaluation tests
│
├── docs/                           # Generated project documentation
│   ├── project-structure.md         # Repository structure (generated)
│   ├── project-parts-metadata.md     # Parts metadata (generated)
│   ├── existing-documentation-inventory.md  # Doc inventory (generated)
│   ├── user-provided-context.md      # User context (generated)
│   ├── technology-stack.md          # Tech stack analysis (generated)
│   ├── architecture-patterns.md      # Architecture patterns (generated)
│   ├── comprehensive-analysis.md      # Pattern analysis (generated)
│   └── project-scan-report.json     # Workflow state (generated)
│
├── htmlcov/                        # Coverage reports (generated)
├── .beads/                         # Beads issue tracking
├── .github/                        # GitHub configuration
│   └── workflows/
│       └── test.yml                 # CI/CD workflow (testing, linting, coverage)
│
├── .venv/                          # Python virtual environment
├── node_modules/                    # Node.js dependencies
├── opencode_customizations.egg-info/  # Python package metadata
│
├── AGENTS.md                       # Agent guidelines and workflow instructions
├── README.md                       # Project overview
├── bun.lock                        # Bun lockfile
├── package.json                    # JavaScript/TypeScript configuration
├── pyproject.toml                  # Python project configuration
├── tsconfig.json                   # TypeScript configuration
└── uv.lock                         # uv lockfile
```

## Critical Directories Summary

### skills/
**Purpose:** Contains Opencode skill packages
**Entry Point:** Each skill has its own entry point
**Integration:** Skills are discovered and loaded by Opencode AI
**Current Skills:**
- `youtube-obsidian/` - Extract YouTube content to Obsidian notes

### _bmad/
**Purpose:** Internal BMAD framework for structured development
**Integration:** Used for project development methodology
**Not Part of Public API:** Internal framework only

### _bmad-output/
**Purpose:** Generated artifacts from BMAD workflows
**Integration:** Reference for planning and implementation
**Contents:** PRD, architecture, epics, workflow status

### scripts/
**Purpose:** Root-level utility scripts
**Integration:** Helper scripts for development and testing
**Entry Point:** `capture_test_data.py` for youtube-obsidian

### evals/
**Purpose:** Evaluation scripts for testing skills
**Integration:** Used to validate skill performance
**Entry Point:** `eval_youtube_obsidian.py`

### docs/
**Purpose:** Generated project documentation
**Integration:** Primary AI retrieval source for brownfield PRD
**Entry Point:** `index.md` (to be generated)

## Entry Points

### YouTube to Obsidian Skill

**Primary Entry Point:** `skills/youtube-obsidian/scripts/get_youtube_data.py`

**Usage:**
```bash
uv run scripts/get_youtube_data.py <youtube_url> "<user_summary>" "<user_comments>"
```

**Environment Variables Required:**
- `YOUTUBE_API_KEY` - YouTube Data API v3 key
- `VAULT_PATH` - Path to Obsidian vault

### Test Scripts

**Unit Tests:** `skills/youtube-obsidian/scripts/test_get_youtube_data.py`
- 30 tests (26 unit + 4 main function)
- 91.30% code coverage
- Tests: URL parsing, metadata fetching, transcript handling, tag generation

**Evaluation:** `evals/eval_youtube_obsidian.py`
- Evaluates skill performance
- Requires test data from `capture_test_data.py`

### CI/CD Entry Point

**GitHub Workflow:** `.github/workflows/test.yml`
- Triggers on push/PR to main, develop
- Runs: tests, coverage, linting, format checks, evals
- Integration tests on main branch only

## Integration Points

### Opencode AI Integration

**Discovery:** Opencode AI discovers skills in `skills/` directory
**Loading:** Each skill's `SKILL.md` provides metadata and usage instructions
**Execution:** Opencode AI runs skill scripts with user-provided parameters

### BMAD Framework Integration

**Project Planning:** BMAD workflows generate PRD, architecture, epics
**Output Location:** `_bmad-output/planning-artifacts/`
**Status Tracking:** `bmm-workflow-status.yaml` tracks workflow progress

### CI/CD Integration

**GitHub Actions:** Automated testing and quality checks
**Coverage Reporting:** Codecov integration for coverage tracking
**Quality Gates:** 80% coverage, ruff linting, format checks

## File Organization Principles

### Skill Package Structure

Each skill follows this structure:
```
skill-name/
├── scripts/              # Implementation
│   ├── main.py          # Entry point
│   ├── test_main.py     # Tests
│   └── conftest.py      # Pytest config
├── test_data/           # Test fixtures
└── SKILL.md            # Documentation
```

### BMAD Framework Structure

```
_bmad/
├── core/               # Core engine
├── bmm/                # Methodology
└── bmb/                # Builder tools
```

### Output Structure

```
_bmad-output/
├── planning-artifacts/   # Planning docs
└── implementation-artifacts/  # Implementation docs
```

## Documentation Structure

### Current Documentation (Generated)

- `project-structure.md` - Directory structure
- `project-parts-metadata.md` - Parts breakdown
- `existing-documentation-inventory.md` - Doc inventory
- `user-provided-context.md` - User context
- `technology-stack.md` - Tech stack
- `architecture-patterns.md` - Architecture
- `comprehensive-analysis.md` - Pattern analysis

### Existing Documentation

- `README.md` - Project overview
- `AGENTS.md` - Agent guidelines
- `skills/youtube-obsidian/SKILL.md` - Skill documentation
- `.github/workflows/test.yml` - CI/CD documentation

## Critical Files Reference

| File | Purpose | Location |
|------|---------|----------|
| **Main Skill Script** | YouTube API integration | `skills/youtube-obsidian/scripts/get_youtube_data.py` |
| **Skill Tests** | Unit tests (30 tests) | `skills/youtube-obsidian/scripts/test_get_youtube_data.py` |
| **Skill Docs** | Complete usage guide | `skills/youtube-obsidian/SKILL.md` |
| **Project Config** | Python package config | `pyproject.toml` |
| **TypeScript Config** | TS compiler settings | `tsconfig.json` |
| **CI/CD Workflow** | Automated testing | `.github/workflows/test.yml` |
| **Agent Guidelines** | Development guidelines | `AGENTS.md` |
| **Workflow Status** | BMAD progress tracking | `_bmad-output/planning-artifacts/bmm-workflow-status.yaml` |

## Notes

- This is a **monolith** repository with **1 part**
- No traditional application entry points (skills are loaded dynamically)
- BMAD framework is internal and not part of public API
- Documentation is generated in `docs/` directory
- Skills are self-contained packages with their own tests
- CI/CD is comprehensive with automated testing and quality checks

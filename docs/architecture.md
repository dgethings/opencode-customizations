# Architecture

## Executive Summary

**opencode-customizations** is a library/package repository that provides customizations and skill packages for Opencode AI. The project follows a modular architecture with self-contained skill packages, internal BMAD methodology framework, and comprehensive testing infrastructure.

**Project Type:** Library/Package Repository  
**Architecture Pattern:** Modular Skill Packages  
**Parts:** 1 (monolith)  
**Primary Language:** Python 3.11+  
**Secondary Language:** TypeScript 5+

## Technology Stack

### Core Technologies

| Component | Technology | Version | Purpose |
|------------|------------|----------|---------|
| **Primary Language** | Python | 3.11+ | Core runtime for skill packages |
| **Secondary Language** | TypeScript | 5+ | Configuration and tooling |
| **JavaScript Runtime** | Bun | latest | Fast JS/TS runtime |
| **Package Manager (Python)** | uv | latest | Fast Python package manager |
| **Build System (Python)** | setuptools | 68.0+ | Python packaging |
| **Testing Framework** | pytest | 8.0+ | Test runner |
| **Code Quality** | ruff | latest | Linter and formatter |
| **Type Checker** | basedpyright | latest | Static type checking |

### Dependencies

**Python Core Dependencies:**
- `requests >= 2.31.0` - HTTP client library
- `youtube-transcript-api >= 0.6.0` - YouTube transcript extraction

**Python Test Dependencies:**
- `pytest >= 8.0.0` - Test framework
- `pytest-mock >= 3.12.0` - Mocking framework
- `pytest-cov >= 4.0.0` - Coverage reporting
- `requests-mock >= 1.12.0` - HTTP mocking

**JavaScript Dependencies:**
- `@types/bun` (dev) - Bun type definitions
- `typescript ^5` (peer) - TypeScript compiler

## Architecture Pattern

### Overall Pattern: Modular Skill Package Repository

The repository follows a **modular library architecture** where:

1. **Skills are self-contained** - Each skill package is independent
2. **Framework is internal** - BMAD methodology is for development use only
3. **Dynamic loading** - Skills are discovered and loaded by Opencode AI
4. **No traditional entry point** - Skills are loaded on-demand

### Architectural Principles

1. **Modularity:** Each skill is independent and self-contained
2. **Reusability:** Skills are designed for reuse across Opencode projects
3. **Extensibility:** New skills can be added without modifying existing code
4. **Type Safety:** Both Python (basedpyright) and TypeScript (strict mode) enforce type safety
5. **Testability:** Comprehensive test coverage with 80% threshold
6. **Documentation-first:** Every skill includes complete SKILL.md documentation

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────┐
│         Opencode AI (External Platform)          │
│                                                  │
│  - Discovers skills in skills/ directory          │
│  - Loads skills dynamically                      │
│  - Executes skill scripts with parameters         │
└──────────────────────┬──────────────────────────┘
                       │
                       │ Uses
                       ▼
┌─────────────────────────────────────────────────────┐
│      opencode-customizations (This Repo)          │
│                                                  │
│  ┌──────────────────────────────────────────────┐ │
│  │  skills/ (Skill Packages)                 │ │
│  │                                          │ │
│  │  ┌──────────────────────────────────────┐  │ │
│  │  │  youtube-obsidian/               │  │ │
│  │  │  - scripts/                      │  │ │
│  │  │  - test_data/                    │  │ │
│  │  │  - SKILL.md                     │  │ │
│  │  └──────────────────────────────────────┘  │ │
│  └──────────────────────────────────────────────┘ │
│                                                  │
│  ┌──────────────────────────────────────────────┐ │
│  │  _bmad/ (Internal Framework)            │ │
│  │  - core/ (Workflow engine)               │ │
│  │  - bmm/ (Methodology)                  │ │
│  │  - bmb/ (Builder tools)                │ │
│  └──────────────────────────────────────────────┘ │
│                                                  │
│  ┌──────────────────────────────────────────────┐ │
│  │  Development/Testing Infrastructure        │ │
│  │  - scripts/ (Utility scripts)           │ │
│  │  - evals/ (Evaluation scripts)         │ │
│  │  - .github/workflows/ (CI/CD)         │ │
│  └──────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

### Component Architecture

#### Skill Package Layer

**Purpose:** Provide reusable functionality for Opencode AI

**Components:**
- **youtube-obsidian** - Extract YouTube content to Obsidian notes
  - Video metadata extraction (YouTube Data API)
  - Transcript retrieval (youtube-transcript-api)
  - Tag generation (auto-generated from content)
  - Obsidian note creation (Markdown with frontmatter)

**Interface:**
- Entry point: `skills/youtube-obsidian/scripts/get_youtube_data.py`
- Parameters: URL, summary, comments
- Output: Obsidian markdown file with frontmatter

#### Internal Framework Layer

**Purpose:** Structured development methodology (not part of public API)

**Components:**
- **core/** - Workflow engine and task execution
- **bmm/** - BMAD methodology workflows (document-project, create-prd, etc.)
- **bmb/** - Builder tools for agents and workflows

**Usage:** Used by agents to follow BMAD methodology during development

#### Infrastructure Layer

**Purpose:** Support development and quality assurance

**Components:**
- **scripts/** - Utility scripts (e.g., capture_test_data.py)
- **evals/** - Evaluation scripts for skill validation
- **.github/workflows/** - CI/CD automation

**Services:**
- Automated testing (pytest)
- Coverage reporting (80% threshold)
- Linting (ruff)
- Formatting (ruff format)
- Type checking (basedpyright)

## Data Architecture

### Skill Data Flow

**YouTube to Obsidian Skill:**

```
┌──────────────┐
│   User       │
│              │
│  YouTube URL │
└──────┬───────┘
       │
       │ Input
       ▼
┌──────────────────────────────────────┐
│  get_youtube_data.py             │
│                                  │
│  1. Extract video ID             │
│  2. Fetch metadata (API)        │
│  3. Get transcript (API)        │
│  4. Generate tags               │
│  5. Create Obsidian note        │
└───────────┬──────────────────────┘
            │
            │ External APIs
            ├──────────────────┐
            ▼                  ▼
┌──────────────────┐  ┌──────────────────┐
│ YouTube Data     │  │ Youtube        │
│ API v3          │  │ Transcript     │
│                 │  │ API            │
│ - Title         │  │                │
│ - Description   │  │ - Transcript    │
│ - Tags          │  │ - Languages    │
└──────────────────┘  └──────────────────┘
            │
            │ Output
            ▼
┌──────────────────────────────────────┐
│  Obsidian Note (Markdown)          │
│                                  │
│  ---                              │
│  title: Video Title               │
│  youtube_id: VIDEO_ID             │
│  tags: [...]                     │
│  ---                              │
│                                  │
│  ## Summary                       │
│  ## Notes                         │
│  ## Description                   │
│  ## Transcript                    │
└──────────────────────────────────────┘
            │
            │ File System
            ▼
┌──────────────────┐
│  Obsidian Vault │
│  (User-specified │
│   directory)     │
└──────────────────┘
```

### Configuration Data

**Environment Variables:**

| Variable | Purpose | Required |
|----------|---------|----------|
| `YOUTUBE_API_KEY` | YouTube Data API v3 key | Yes (for youtube-obsidian) |
| `VAULT_PATH` | Path to Obsidian vault | Yes (for youtube-obsidian) |

**Configuration Files:**

- `pyproject.toml` - Python project configuration, dependencies, testing
- `tsconfig.json` - TypeScript compiler configuration
- `package.json` - JavaScript/TypeScript dependencies
- `uv.lock` - Python dependency lockfile
- `bun.lock` - JavaScript dependency lockfile

### Test Data

**Location:** `skills/youtube-obsidian/test_data/`

**Purpose:** Fixtures for unit tests

**Content:** Mocked API responses, test URLs, expected outputs

## Component Overview

### YouTube to Obsidian Skill

**Location:** `skills/youtube-obsidian/`

**Components:**

**Scripts:**
- `get_youtube_data.py` - Main entry point
  - Extract video ID from URL
  - Fetch video metadata (title, description, tags)
  - Retrieve transcript
  - Generate tags (max 15)
  - Create Obsidian note with frontmatter

**Tests:**
- `test_get_youtube_data.py` - Comprehensive test suite
  - 30 tests (26 unit + 4 main function)
  - 91.30% code coverage
  - Tests: URL parsing, metadata fetching, transcript handling, tag generation

**Documentation:**
- `SKILL.md` - Complete usage guide
  - Prerequisites and setup
  - Workflow explanation
  - Testing instructions
  - Error handling

**External APIs:**
- YouTube Data API v3 - Metadata fetching
- youtube-transcript-api - Transcript retrieval

### BMAD Framework (Internal)

**Location:** `_bmad/`

**Components:**

**core/** - Workflow Engine
- Task execution engine
- Workflow orchestration
- Agent management

**bmm/** - BMAD Methodology
- document-project workflow
- create-prd workflow
- create-architecture workflow
- create-epics-and-stories workflow
- Implementation-readiness workflow

**bmb/** - Builder Module
- Agent creation workflows
- Workflow builder tools
- Architecture templates

**Usage:** Used by agents for structured project development

**Note:** Not part of public API - internal methodology framework only

### Development Infrastructure

**scripts/** - Utility Scripts

- `capture_test_data.py` - Capture real API data for testing
  - Fetches video data from YouTube API
  - Saves to test_data directory
  - Used to create realistic test fixtures

**evals/** - Evaluation Scripts

- `eval_youtube_obsidian.py` - Skill evaluation
  - Evaluates skill performance
  - Validates accuracy
  - Generates evaluation report
  - Requires >90% accuracy

**.github/workflows/test.yml** - CI/CD Pipeline

- Runs on: push to main/develop, PR to main/develop
- Stages:
  1. Unit tests (mocked APIs)
  2. Coverage check (80% threshold)
  3. Linting (ruff check)
  4. Format check (ruff format)
  5. Evaluation script
  6. Coverage upload to Codecov
  7. Integration tests (main branch only, with real API)

## Source Tree

```
opencode-customizations/
├── skills/                      # Skill packages
│   └── youtube-obsidian/
│       ├── scripts/              # Implementation
│       ├── test_data/            # Test fixtures
│       └── SKILL.md             # Documentation
│
├── _bmad/                      # Internal framework
│   ├── core/                   # Workflow engine
│   ├── bmm/                    # Methodology
│   └── bmb/                    # Builder tools
│
├── _bmad-output/               # Generated artifacts
│   ├── planning-artifacts/        # PRD, architecture, epics
│   └── implementation-artifacts/ # Implementation docs
│
├── scripts/                     # Utility scripts
├── evals/                       # Evaluation scripts
├── docs/                        # Generated documentation
│
├── AGENTS.md                    # Agent guidelines
├── pyproject.toml               # Python config
├── tsconfig.json                # TypeScript config
├── package.json                 # JavaScript config
└── .github/workflows/test.yml   # CI/CD
```

## Development Workflow

### Skill Development Lifecycle

```
1. Create Skill
   └── mkdir skills/<skill-name>/
       mkdir scripts/
       touch SKILL.md

2. Implement
   └── Write scripts/main.py
       Write scripts/test_main.py

3. Test
   └── uv run pytest -v
       uv run pytest --cov=<skill>/scripts --cov-fail-under=80

4. Quality Checks
   └── uv run ruff check .
       uv run ruff format .
       basedpyright

5. Documentation
   └── Complete SKILL.md
       Add docstrings to code

6. CI/CD
   └── Push to GitHub
       GitHub Actions runs automatically
       All checks must pass

7. Integration
   └── Opencode AI discovers skill
       Loads dynamically
       Executes on-demand
```

### Quality Gates

Before merging:

1. ✅ All tests pass (pytest)
2. ✅ Coverage ≥ 80% (pytest-cov)
3. ✅ No linting errors (ruff check)
4. ✅ Code formatted (ruff format)
5. ✅ Type checking passes (basedpyright)
6. ✅ Evaluation passes (eval script)
7. ✅ Documentation complete (SKILL.md)
8. ✅ Code reviewed

## Deployment Architecture

**No Traditional Deployment**

This is a library/package repository:

- Skills are used by Opencode AI (external platform)
- BMAD framework is for internal development use only
- Documentation is generated locally
- No production deployment required

### Skill Distribution

**Manual Integration Process:**

1. Develop skill in `skills/<skill-name>/`
2. Test and evaluate locally
3. Push to GitHub (CI/CD validates)
4. Opencode AI discovers skill automatically
5. Skill is available for use

### Documentation Generation

**BMAD Workflows:**

- Run BMAD workflows to generate PRD, architecture, epics
- Output to `_bmad-output/planning-artifacts/`
- Reference documentation from `docs/`

**Project Documentation:**

- Run document-project workflow
- Output to `docs/`
- Primary AI retrieval source for brownfield PRD

## Testing Strategy

### Test Pyramid

```
           ┌──────────┐
           │  Evals   │  High-level skill evaluation
           └──────────┘
                │
           ┌──────────┐
           │ Integration│ Real API tests (main only)
           └──────────┘
                │
           ┌──────────┐
           │  Unit    │ Comprehensive unit tests
           └──────────┘
```

### Testing Tools

- **pytest** - Test runner
- **pytest-mock** - Mocking framework
- **requests-mock** - HTTP mocking
- **pytest-cov** - Coverage reporting

### Coverage Requirements

- **Minimum:** 80%
- **Current:** 91.30% (youtube-obsidian skill)
- **Target:** Maintain >90%

### Test Organization

```
skills/youtube-obsidian/scripts/
├── get_youtube_data.py          # Implementation
├── test_get_youtube_data.py     # Tests
│   ├── TestExtractVideoId        # URL parsing tests
│   ├── TestFetchMetadata        # API fetching tests
│   ├── TestGetTranscript       # Transcript tests
│   ├── TestGenerateTags         # Tag generation tests
│   ├── TestCreateObsidianNote  # Note creation tests
│   └── TestIntegration         # Real API tests
└── conftest.py                # Pytest fixtures
```

## Security Architecture

### API Key Management

**Storage:**
- Environment variables only
- GitHub Secrets (YOUTUBE_API_KEY)
- Never committed to repository

**Usage:**
```python
api_key = os.environ.get("YOUTUBE_API_KEY")
if not api_key:
    print("Error: YOUTUBE_API_KEY not set")
    sys.exit(1)
```

### Input Validation

**URL Validation:**
```python
def extract_video_id(url: str) -> str:
    """Extract and validate video ID."""
    if not url or not isinstance(url, str):
        raise ValueError("URL must be a non-empty string")
    # ... extraction and validation
```

**Error Handling:**
- Specific exceptions with helpful messages
- Wrap external API calls in try/except
- Validate all user inputs

### Dependency Security

- Regular dependency updates via `uv`
- Review GitHub security advisories
- Use Dependabot (if enabled)

## Performance Considerations

### Skill Performance

**YouTube to Obsidian:**
- API calls: 2 (metadata + transcript)
- Processing time: <5 seconds typical
- Memory usage: Low (streaming transcript)

### Optimization Strategies

1. **Lazy Loading:** Skills loaded on-demand
2. **Streaming:** Large transcripts processed in chunks
3. **Caching:** API responses cached in tests
4. **Minimal Dependencies:** Only essential packages

## Scalability

### Adding New Skills

**Process:**
1. Create skill directory
2. Implement scripts
3. Write tests (80%+ coverage)
4. Document (SKILL.md)
5. Push to GitHub
6. Automatically discovered by Opencode AI

**Effort:** ~2-4 hours for typical skill

### Test Scalability

- Tests isolated per skill
- No cross-skill dependencies
- Parallel execution possible

### Documentation Scalability

- Each skill has own SKILL.md
- Project docs generated once
- Easy to maintain

## Monitoring and Observability

### CI/CD Monitoring

- GitHub Actions dashboard
- Test pass/fail rates
- Coverage trends (Codecov)
- Build duration

### Evaluation Metrics

- Skill accuracy (>90% required)
- Test execution time
- Resource usage

## Future Considerations

### Potential Enhancements

1. **Automated Testing:** Add more integration tests
2. **Documentation:** Add interactive examples
3. **Skills:** Add more skill packages
4. **CI/CD:** Add automated skill validation
5. **Monitoring:** Add performance metrics

### Architectural Evolution

- Consider skill registry for better discoverability
- Add skill versioning
- Implement skill dependency management
- Add automated skill testing pipeline

## Summary

| Aspect | Details |
|---------|---------|
| **Architecture** | Modular skill package library |
| **Pattern** | Self-contained, reusable skills |
| **Languages** | Python 3.11+ (primary), TypeScript 5+ (config) |
| **Entry Points** | Skill-specific (no global entry point) |
| **Testing** | pytest with 80%+ coverage |
| **Quality** | ruff, basedpyright, eval scripts |
| **CI/CD** | GitHub Actions with automated checks |
| **Deployment** | Library distribution (no deployment) |
| **Documentation** | SKILL.md per skill + project docs |

# Architecture Patterns

## Project Architecture

### Overall Pattern: Library/Package Repository

This project follows a **library/package repository architecture**, designed to provide reusable skill packages and customizations for Opencode AI.

### Architectural Style

**Modular Package System:**
- **Package-based structure**: Each skill is a standalone package
- **Multi-language support**: Python and TypeScript coexist
- **Separation of concerns**: Skills, scripts, evaluations, and framework are isolated
- **Framework integration**: BMAD methodology framework for structured development

### Key Architectural Principles

1. **Modularity**: Each skill is independent and self-contained
2. **Reusability**: Skills are designed to be reused across different Opencode projects
3. **Extensibility**: New skills can be added without modifying existing code
4. **Type Safety**: Both Python (basedpyright) and TypeScript (strict mode) enforce type safety
5. **Testability**: Comprehensive test coverage with 80% threshold
6. **Documentation-first**: Every skill includes complete SKILL.md documentation

### Component Architecture

```
opencode-customizations/
│
├── skills/                    # Skill packages (reusable components)
│   └── youtube-obsidian/     # Example skill package
│       ├── scripts/          # Skill implementation
│       ├── test_data/        # Test fixtures
│       └── SKILL.md          # Skill documentation
│
├── _bmad/                    # BMAD framework (internal methodology)
│   ├── bmm/                  # Methodology workflows
│   └── core/                 # Core workflow engine
│
├── _bmad-output/             # Generated artifacts
│   └── planning-artifacts/   # PRD, architecture, epics
│
├── scripts/                  # Root-level utility scripts
├── evals/                    # Evaluation scripts for testing
├── docs/                     # Generated documentation
└── .beads/                   # Issue tracking
```

### Data Flow

1. **Skill Development Flow:**
   - Create skill directory in `skills/`
   - Implement Python scripts
   - Write comprehensive tests (80% coverage)
   - Document with SKILL.md
   - Test with pytest and eval scripts

2. **Documentation Flow:**
   - BMAD workflows generate documentation
   - Output to `_bmad-output/planning-artifacts/`
   - Reference documentation from `docs/`

3. **CI/CD Flow:**
   - GitHub Actions triggers on push/PR
   - Run unit tests with mocked APIs
   - Check coverage threshold
   - Run linting and format checks
   - Execute evaluation scripts
   - Run integration tests (main branch only)

### Technology Stack Architecture

**Dual-Language Architecture:**

```
┌─────────────────────────────────────────┐
│         Opencode Customizations        │
└─────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
┌──────────────┐        ┌──────────────┐
│   Python     │        │  TypeScript  │
│   Skills     │        │  Config     │
│   Runtime    │        │  Tooling    │
└──────────────┘        └──────────────┘
        │                       │
        │                       │
        ▼                       ▼
┌──────────────┐        ┌──────────────┐
│   setuptools │        │     Bun      │
│   packaging  │        │   Runtime    │
└──────────────┘        └──────────────┘
```

### Integration Points

- **BMAD Framework**: Internal methodology for project development
- **Opencode AI**: External platform that uses these customizations
- **GitHub Actions**: CI/CD integration for automated testing
- **Codecov**: Coverage reporting integration

### Testing Strategy

**Test Pyramid:**

```
        ┌─────────────┐
        │  Evals      │  High-level skill evaluation
        └─────────────┘
              │
        ┌─────────────┐
        │ Integration │  Real API tests (main only)
        └─────────────┘
              │
        ┌─────────────┐
        │   Unit      │  Comprehensive unit tests (80%+)
        └─────────────┘
```

**Testing Tools:**
- **pytest**: Test runner
- **pytest-mock**: Mocking framework
- **requests-mock**: HTTP mocking
- **pytest-cov**: Coverage reporting

### Quality Gates

1. **Code Coverage**: Minimum 80%
2. **Linting**: ruff check must pass
3. **Formatting**: ruff format must be consistent
4. **Type Checking**: basedpyright must pass
5. **Tests**: All unit tests must pass
6. **Evaluation**: Evaluation scripts must pass

### Deployment Architecture

**No traditional deployment** - this is a library/package repository:
- Skills are used by Opencode AI (external platform)
- BMAD workflows generate documentation locally
- GitHub Actions validates code quality on every push
- No production deployment required

### Scalability Considerations

- **Skill Addition**: New skills can be added independently
- **Test Scalability**: Tests are isolated per skill
- **Documentation**: Each skill has its own documentation
- **CI/CD**: Matrix testing can be extended for Python versions

### Security Considerations

- **API Keys**: Stored as GitHub secrets (YOUTUBE_API_KEY)
- **No sensitive data**: Skills don't store credentials
- **Dependency management**: Regular updates via uv
- **Code review**: PR-based workflow with CI checks

### Maintenance Strategy

- **Automated Testing**: CI on every push/PR
- **Coverage Tracking**: Continuous coverage reporting
- **Quality Checks**: Automated linting and formatting
- **Documentation**: SKILL.md for every skill
- **Issue Tracking**: Beads integration

## Architecture Summary

| Aspect | Pattern |
|--------|---------|
| **Overall** | Library/Package Repository |
| **Organization** | Modular with skill packages |
| **Languages** | Dual: Python 3.11+ + TypeScript 5+ |
| **Packaging** | setuptools (Python) + Bun (TypeScript) |
| **Testing** | pytest with 80% coverage |
| **Quality** | ruff + basedpyright |
| **CI/CD** | GitHub Actions |
| **Documentation** | SKILL.md per skill |
| **Deployment** | Library distribution (no deployment) |

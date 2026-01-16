# Technology Stack

## Overview

This is a **dual-language project** (Python + TypeScript) that provides customizations and skill packages for Opencode AI.

## Technology Table

| Category | Technology | Version | Justification |
|----------|-----------|---------|---------------|
| **Primary Language** | Python | 3.11+ | Core runtime for skill packages and scripts |
| **Secondary Language** | TypeScript | 5+ | Type-safe configuration and tooling |
| **JavaScript Runtime** | Bun | latest | Fast JavaScript/TypeScript runtime |
| **Python Package Manager** | uv | latest | Fast Python package installer/manager |
| **Python Build System** | setuptools | 68.0+ | Standard Python packaging |
| **Testing Framework** | pytest | 8.0+ | Python test runner |
| **Coverage Tool** | pytest-cov | 4.0+ | Test coverage reporting |
| **Mocking Framework** | pytest-mock | 3.12+ | Test mocking |
| **HTTP Client** | requests | 2.31.0+ | HTTP library for Python |
| **YouTube API Library** | youtube-transcript-api | 0.6.0+ | YouTube video transcript extraction |
| **Code Quality** | ruff | latest | Fast Python linter and formatter |
| **Type Checker** | basedpyright | latest | Static type checking for Python |
| **CI/CD** | GitHub Actions | - | Automated testing and linting |

## Architecture Pattern

**Pattern:** Library/Package Repository

**Justification:**
- Package-based structure with reusable skills
- Multiple language support (Python + TypeScript)
- Modular design with skill packages
- Standard Python packaging (setuptools)
- Module-based TypeScript configuration
- Focus on reusability and extensibility

## Dependencies

### Python Dependencies

```toml
[project.dependencies]
- requests >= 2.31.0
- youtube-transcript-api >= 0.6.0

[project.optional-dependencies.test]
- pytest >= 8.0.0
- pytest-mock >= 3.12.0
- pytest-cov >= 4.0.0
- requests-mock >= 1.12.0
```

### JavaScript/TypeScript Dependencies

```json
{
  "devDependencies": {
    "@types/bun": "latest"
  },
  "peerDependencies": {
    "typescript": "^5"
  }
}
```

## Development Tools

### Code Quality

- **ruff**: Fast Python linter and formatter
  - Line length: 88 characters
  - Target version: Python 3.11
  - Checks: E (errors), F (pyflakes), I (isort), N (naming), W (warnings), UP (pyupgrade)

- **basedpyright**: Static type checker
  - Mode: Standard type checking
  - Strict type enforcement

### Testing

- **pytest**: Test runner with 80% coverage threshold
- **pytest-mock**: Mocking framework for tests
- **requests-mock**: HTTP mocking for API tests

### Package Management

- **uv**: Fast Python package manager
- **Bun**: Fast JavaScript runtime and package manager

## Build and Packaging

- **Python**: setuptools with custom package discovery (skills*)
- **TypeScript**: ESNext target, bundler mode, strict mode enabled
- **Format**: JavaScript ES modules (type: "module")

## CI/CD Configuration

GitHub Actions workflow (`test.yml`):
- Python 3.11 matrix
- uv-based installation
- Unit tests with mocked APIs
- Coverage threshold enforcement (80%)
- Linting (ruff check)
- Format checking (ruff format --check)
- Evaluation script execution
- Integration tests with real YouTube API (main branch only)
- Codecov coverage upload

## Technology Stack Summary

**Primary Stack:** Python 3.11+ with setuptools packaging
**Secondary Stack:** TypeScript 5+ with Bun runtime
**Testing:** pytest with 80% coverage requirement
**Quality:** ruff (linting/formatting) + basedpyright (type checking)
**CI/CD:** GitHub Actions with automated testing
**Package Management:** uv (Python) + Bun (JavaScript/TypeScript)

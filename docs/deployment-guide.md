# Deployment Guide

## Overview

This is a **library/package repository** with no traditional deployment. Skills are used by Opencode AI (external platform), and BMAD workflows generate documentation locally. This guide covers CI/CD configuration and distribution processes.

## Architecture

**No Production Deployment Required:**

This repository provides:
1. **Skill packages** for Opencode AI (consumed externally)
2. **BMAD framework** for development methodology (internal)
3. **Generated documentation** (local output)

## CI/CD Pipeline

### GitHub Actions Workflow

**Location:** `.github/workflows/test.yml`

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

### Pipeline Stages

#### 1. Unit Tests (All Branches)

```yaml
- name: Run unit tests with mocked APIs
  run: |
    uv run pytest skills/youtube-obsidian/scripts/test_get_youtube_data.py \
      -v \
      --cov=skills/youtube-obsidian/scripts \
      --cov-report=xml \
      --cov-report=term-missing
```

**Requirements:**
- Python 3.11
- All dependencies installed
- Tests use mocked APIs (no external calls)

**Success Criteria:**
- All tests pass
- Coverage report generated

#### 2. Coverage Threshold Check

```yaml
- name: Check coverage threshold
  run: |
    uv run pytest skills/youtube-obsidian/scripts/test_get_youtube_data.py \
      --cov=skills/youtube-obsidian/scripts \
      --cov-fail-under=80
```

**Threshold:** 80% minimum coverage

**Failure:** Pipeline fails if coverage < 80%

#### 3. Linting

```yaml
- name: Run linting
  run: |
    uv run ruff check .
```

**Checks:**
- Code style errors (E)
- Pyflakes (F)
- Import sorting (I)
- Naming conventions (N)
- Warnings (W)
- Code upgrades (UP)

**Failure:** Pipeline fails if linting errors found

#### 4. Format Check

```yaml
- name: Run format check
  run: |
    uv run ruff format --check .
```

**Checks:**
- Code formatting consistency
- Line length (88 characters)
- Indentation (4 spaces for Python)
- File endings

**Failure:** Pipeline fails if formatting issues found

#### 5. Evaluation Script

```yaml
- name: Run eval script
  run: |
    uv run evals/eval_youtube_obsidian.py
```

**Purpose:**
- Evaluates skill performance
- Validates skill accuracy
- Ensures quality standards

**Failure:** Pipeline fails if evaluation fails

#### 6. Coverage Upload

```yaml
- name: Upload coverage to Codecov
  if: matrix.python-version == '3.11'
  uses: codecov/codecov-action@v4
  with:
    file: ./coverage.xml
    flags: unittests
    name: codecov-umbrella
    fail_ci_if_error: false
```

**Uploads:**
- Coverage XML report
- Flagged as "unittests"
- Does not fail CI on upload error

#### 7. Integration Tests (Main Branch Only)

```yaml
integration:
  runs-on: ubuntu-latest
  if: github.event_name == 'push' && github.ref == 'refs/heads/main'

  steps:
    - name: Run integration tests with real API
      if: env.YOUTUBE_API_KEY != ''
      env:
        YOUTUBE_API_KEY: ${{ secrets.YOUTUBE_API_KEY }}
      run: |
        uv run pytest skills/youtube-obsidian/scripts/test_get_youtube_data.py::TestIntegration -v
      continue-on-error: true
```

**Conditions:**
- Only runs on push to `main` branch
- Requires `YOUTUBE_API_KEY` GitHub secret
- Uses real YouTube API (not mocked)

**Failure:** Continues on error (non-blocking)

### Secrets Configuration

**Required Secrets (GitHub Repository Settings):**

| Secret Name | Purpose | Required |
|-------------|---------|----------|
| `YOUTUBE_API_KEY` | YouTube Data API v3 key | Optional (integration tests only) |

**Setting Secrets:**

1. Go to repository Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add `YOUTUBE_API_KEY` with your API key
4. Integration tests will use this secret

### Environment Variables

**GitHub Actions Environment:**

```yaml
env:
  YOUTUBE_API_KEY: ${{ secrets.YOUTUBE_API_KEY }}
```

**Local Development:**

```bash
export YOUTUBE_API_KEY="your-api-key"
export VAULT_PATH="/path/to/vault"
```

## Distribution

### Skill Distribution to Opencode AI

**No Automated Distribution:**

Skills are manually integrated with Opencode AI:

1. **Develop skill** in `skills/<skill-name>/`
2. **Test skill** locally with pytest
3. **Evaluate skill** with eval scripts
4. **Document skill** with SKILL.md
5. **Push to GitHub** (triggers CI/CD)
6. **Manually integrate** with Opencode AI

**Integration Process:**

Opencode AI discovers skills based on:
- Directory structure (`skills/`)
- SKILL.md frontmatter
- Script entry points

### Python Package Distribution (Optional)

**Publish to PyPI (if desired):**

```bash
# Build package
uv build

# Publish to PyPI (requires API token)
uv publish

# Or use twine
pip install build twine
python -m build
twine upload dist/*
```

**Requirements:**
- Valid version in `pyproject.toml`
- PyPI API token configured
- Package passes all tests

### Documentation Distribution

**BMAD Documentation:**

Generated locally in `_bmad-output/planning-artifacts/`:

- `prd.md` - Product Requirements Document
- `architecture.md` - Architecture document
- `epics.md` - Epics and stories

**Project Documentation:**

Generated locally in `docs/`:

- `project-structure.md`
- `technology-stack.md`
- `architecture-patterns.md`
- `comprehensive-analysis.md`
- `source-tree-analysis.md`
- `development-guide.md`
- etc.

**No automated deployment** - documentation is generated locally and referenced by workflows.

## Quality Gates

### Pre-Merge Requirements

All of the following must pass before merging to main:

1. ✅ **All tests pass** (pytest)
2. ✅ **Coverage ≥ 80%** (pytest-cov)
3. ✅ **No linting errors** (ruff check)
4. ✅ **Code formatted** (ruff format)
5. ✅ **Evaluation passes** (eval script)
6. ✅ **Code review approved**

### Integration Test Requirements (Main Branch)

Optional but recommended:

- ✅ **Integration tests pass** (with real API)
- ✅ **Coverage uploaded** to Codecov

### Release Requirements

Before tagging a release:

1. ✅ **Update version** in `pyproject.toml`
2. ✅ **Update CHANGELOG** (if exists)
3. ✅ **All quality gates pass**
4. ✅ **Tests pass** on main branch
5. ✅ **Code reviewed**
6. ✅ **Create git tag**

## Monitoring

### CI/CD Monitoring

**GitHub Actions Dashboard:**

1. Go to repository → Actions
2. View workflow runs
3. Check for failures
4. Review logs

**Key Metrics:**
- Test pass rate
- Coverage percentage
- Linting errors
- Format issues
- Build duration

### Coverage Monitoring

**Codecov Dashboard:**

1. Go to Codecov for repository
2. View coverage trends
3. Identify uncovered code
4. Track improvement

### Issue Tracking

**Beads Integration:**

```bash
# Show ready issues
bd ready

# Show all issues
bd list --all

# Show issue details
bd show <issue-id>
```

## Rollback Procedures

### Rollback Process

**If a merge causes issues:**

1. **Identify problematic commit**
2. **Create revert commit:**

```bash
git revert <commit-hash>
git push origin main
```

3. **Or revert to previous tag:**

```bash
git checkout <previous-tag>
git checkout -b main-fix
git push origin main-fix
```

4. **Update GitHub Actions** if necessary
5. **Monitor CI/CD** for successful run

### Hotfix Process

1. **Create hotfix branch:**

```bash
git checkout -b hotfix/<issue-description>
```

2. **Implement fix**
3. **Test locally**
4. **Push and run CI/CD**
5. **Merge to main**
6. **Create hotfix tag**

## Security Considerations

### API Key Management

**Never Commit API Keys:**

- Add `YOUTUBE_API_KEY` to GitHub secrets
- Use environment variables in CI/CD
- Use `.env` files locally (gitignored)

**Validating Secrets:**

```yaml
# Check secret exists before use
- name: Run integration tests with real API
  if: env.YOUTUBE_API_KEY != ''
```

### Dependency Security

**Regular Updates:**

```bash
# Update Python dependencies
uv pip install --upgrade -e ".[test]"

# Update JavaScript dependencies
bun update
```

**Vulnerability Scanning:**

- Use GitHub Dependabot (if enabled)
- Review security alerts
- Update vulnerable dependencies

### Code Security

**Best Practices:**

1. Never commit secrets or credentials
2. Use environment variables for sensitive data
3. Validate user input
4. Use parameterized queries (if using databases)
5. Review dependencies for vulnerabilities

## Troubleshooting

### CI/CD Failures

**Tests Failing:**

```bash
# Run tests locally
uv run pytest -v

# Check coverage
uv run pytest --cov=skills/youtube-obsidian/scripts --cov-report=term-missing
```

**Coverage Below 80%:**

```bash
# Identify uncovered lines
uv run pytest --cov=skills/youtube-obsidian/scripts --cov-report=term-missing

# Add tests for uncovered code
```

**Linting Errors:**

```bash
# Auto-fix linting issues
uv run ruff check --fix .

# Format code
uv run ruff format .
```

**Format Check Failing:**

```bash
# Format code
uv run ruff format .

# Check format
uv run ruff format --check .
```

**Evaluation Failing:**

```bash
# Run evaluation locally
uv run evals/eval_youtube_obsidian.py

# Check evaluation logs for issues
```

### Integration Test Failures

**API Key Issues:**

1. Check GitHub secret `YOUTUBE_API_KEY` is set
2. Verify API key is valid
3. Check YouTube Data API v3 is enabled

**Rate Limiting:**

- YouTube API has rate limits
- Integration tests may fail if limit exceeded
- Wait for quota to reset or increase quota

## Best Practices

1. **Run tests locally** before pushing
2. **Maintain 80%+ coverage** threshold
3. **Fix linting issues** before committing
4. **Format code** consistently
5. **Review CI/CD logs** for failures
6. **Monitor coverage trends** on Codecov
7. **Update dependencies** regularly
8. **Never commit secrets** or API keys
9. **Use feature branches** for development
10. **Create pull requests** for code review

## Summary

| Aspect | Details |
|--------|---------|
| **Deployment Type** | Library/package repository |
| **Production Deployment** | None required |
| **CI/CD** | GitHub Actions (test.yml) |
| **Quality Gates** | 80% coverage, linting, formatting |
| **Distribution** | Manual integration with Opencode AI |
| **Monitoring** | GitHub Actions, Codecov, Beads |
| **Rollback** | Git revert or hotfix branch |

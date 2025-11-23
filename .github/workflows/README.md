# GitHub Actions Workflows for YarnGPT SDK

This directory contains GitHub Actions workflows for automated testing, linting, and publishing.

## Workflows

### 1. **test.yml** - Automated Testing

- **Trigger:** Push/PR to main, master, or develop branches
- **What it does:**
  - Tests on Ubuntu, Windows, and macOS
  - Tests Python 3.8, 3.9, 3.10, 3.11, and 3.12
  - Runs unit tests (skips integration tests that need API key)
  - Validates package can be built
- **No secrets required** ✓

### 2. **lint.yml** - Code Quality Checks

- **Trigger:** Push/PR to main, master, or develop branches
- **What it does:**
  - Runs ruff linting
  - Checks code formatting
  - Runs mypy type checking
- **No secrets required** ✓

### 3. **publish-test.yml** - Publish to TestPyPI

- **Trigger:** Push to develop branch or manual trigger
- **What it does:**
  - Runs tests
  - Builds package
  - Publishes to TestPyPI for testing
- **Requires:** `TEST_PYPI_API_TOKEN` secret

### 4. **publish.yml** - Publish to PyPI

- **Trigger:** When you create a GitHub release or manual trigger
- **What it does:**
  - Runs tests
  - Builds package with uv
  - Publishes to PyPI
- **Requires:** `PYPI_API_TOKEN` secret

## Setup Instructions

### For Testing and Linting (No secrets needed!)

These workflows work automatically once you push to GitHub. No configuration required.

### For Publishing to PyPI

#### 1. Get PyPI API Token

1. Create account on [PyPI](https://pypi.org)
2. Go to Account Settings → API tokens
3. Create a new API token with scope for this project
4. Copy the token (starts with `pyp-...`)

#### 2. Add Secret to GitHub

1. Go to your repository on GitHub
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Name: `PYPI_API_TOKEN`
5. Value: Paste your PyPI token
6. Click "Add secret"

#### 3. (Optional) Setup TestPyPI

For testing releases before publishing to real PyPI:

1. Create account on [TestPyPI](https://test.pypi.org)
2. Get API token from TestPyPI
3. Add as `TEST_PYPI_API_TOKEN` secret in GitHub

## Publishing Process

### Test Release (to TestPyPI)

```bash
# Push to develop branch
git push origin develop
```

Or trigger manually in GitHub Actions tab

### Production Release (to PyPI)

1. Update version in `pyproject.toml`
2. Commit and push changes
3. Create a GitHub release:

   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```

4. Go to GitHub → Releases → Create new release
5. Select the tag, add release notes
6. Publish release
7. GitHub Actions will automatically build and publish to PyPI!

### Manual Publish

You can also trigger publishing manually:

1. Go to Actions tab in GitHub
2. Select "Publish to PyPI" workflow
3. Click "Run workflow"

## Building Locally with uv

```bash
# Build the package
uv build

# Check the built package
ls dist/

# Test install locally
uv pip install dist/yarngpt_sdk-0.1.0-py3-none-any.whl

# Publish manually (if needed)
uv publish
```

## Workflow Status Badges

Add these to your README.md:

```markdown
[![Tests](https://github.com/hallelx2/yarngpt-sdk/actions/workflows/test.yml/badge.svg)](https://github.com/hallelx2/yarngpt-sdk/actions/workflows/test.yml)
[![Code Quality](https://github.com/hallelx2/yarngpt-sdk/actions/workflows/lint.yml/badge.svg)](https://github.com/hallelx2/yarngpt-sdk/actions/workflows/lint.yml)
```

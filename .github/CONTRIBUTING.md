# GitHub CI/CD Configuration

This project uses GitHub Actions for automated building and publishing.

## Workflows

### Build Workflow (`build.yml`)

Runs on every push to `main` and `develop` branches, and on pull requests.

**What it does:**
- Sets up Python 3.13
- Installs dependencies using `uv`
- Builds the package (wheel + sdist)
- Validates build artifacts exist
- Tests CLI basic functionality
- Uploads build artifacts

### Publish Workflow (`publish.yml`)

Runs automatically when a release is published on GitHub.

**What it does:**
- Sets up Python 3.13
- Builds the package
- Publishes to PyPI using the `PYPI_API_TOKEN` secret

## Setup Instructions

### 1. Configure PyPI Publishing

To enable automatic publishing to PyPI:

1. Generate a PyPI API token:
   - Go to https://pypi.org/manage/account/token/
   - Create a new token with "Entire account" scope
   - Copy the token

2. Add the token as a GitHub secret:
   - Go to your GitHub repository settings
   - Navigate to **Secrets and variables** → **Actions**
   - Click **New repository secret**
   - Name: `PYPI_API_TOKEN`
   - Value: paste your PyPI token
   - Click **Add secret**

### 2. Creating a Release

To publish a new version:

1. Update the version in `pyproject.toml`:
   ```toml
   version = "0.2.0"
   ```

2. Commit and push the version change

3. Create a GitHub release:
   - Go to your repository on GitHub
   - Click **Releases**
   - Click **Draft a new release**
   - Enter a tag (e.g., `v0.2.0`)
   - Add release notes
   - Click **Publish release**

The publish workflow will automatically run and publish to PyPI.

## Troubleshooting

### Build fails

Check the workflow logs in the **Actions** tab:
- Verify Python 3.13 is available
- Check for dependency issues
- Ensure `uv` can resolve all dependencies

### Publish fails

Common issues:
- `PYPI_API_TOKEN` secret not configured
- Version already exists on PyPI
- Package metadata issues (check `pyproject.toml`)

## Local Testing

To test the build locally:

```bash
# Install uv if not already installed
# Build the package
uv build

# Verify artifacts
ls -la dist/
```

To test the CLI:

```bash
uv run glissade --help
uv run python -m glissade --help
```

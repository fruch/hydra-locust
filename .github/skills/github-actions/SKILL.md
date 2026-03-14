---
name: github-actions
description: >-
  Author and maintain GitHub Actions workflows for CI/CD pipelines. Use when
  creating new workflows, modifying CI configuration, adding workflow jobs,
  configuring matrix builds, setting up caching, managing secrets, writing
  workflow_run triggers, or debugging GitHub Actions issues. Covers CI,
  testing, and release workflows for hydra-locust.
---

# GitHub Actions Workflow Authoring

Author, maintain, and debug GitHub Actions workflows for the hydra-locust project. All workflows live in `.github/workflows/`.

## Before Starting

1. Read any existing CI workflow in `.github/workflows/`
2. Check related plans for workflow requirements:
   - `docs/plans/03-testing-strategy.md` — CI and testing strategy
   - `docs/plans/high-level-design.md` — Project overview

## Planned Workflows

| Workflow | File | Trigger | Status |
|----------|------|---------|--------|
| CI | `ci.yml` | push to main, PRs | Planned |
| CI Failure Analysis | `ci-failure-analysis.yml` | workflow_run (CI failed) | Planned |
| Release | `release.yml` | tag push (v*) | Planned |

## Workflow Conventions

### Standard Job Structure

Every job should follow this pattern:

```yaml
jobs:
  job-name:
    name: Human-Readable Name
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v6
        with:
          version: "latest"
      - run: uv sync --dev
      - run: uv run <command>
```

### Caching

`astral-sh/setup-uv` handles caching automatically. For additional caching:

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.cache/uv
    key: ${{ runner.os }}-uv-${{ hashFiles('uv.lock') }}
```

### Environment Variables

Set project-wide env vars at the workflow level:

```yaml
env:
  UV_SYSTEM_PYTHON: 1
  PYTHONDONTWRITEBYTECODE: 1
```

### Permissions

Follow the principle of least privilege:

```yaml
# Read-only (default for most CI jobs)
permissions:
  contents: read

# PR commenting (failure analysis)
permissions:
  contents: read
  pull-requests: write
  actions: read
```

## CI Jobs

### Lint Job

```yaml
lint:
  name: Lint
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: astral-sh/setup-uv@v6
    - run: uv sync --dev
    - run: uv run ruff check .
    - run: uv run ruff format --check .
```

### Test Job

```yaml
test:
  name: Test
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: astral-sh/setup-uv@v6
    - run: uv sync --dev
    - run: uv run pytest --junitxml=test-results.xml
    - uses: actions/upload-artifact@v4
      if: always()
      with:
        name: test-results
        path: test-results.xml
```

### Integration Test Job

```yaml
integration:
  name: Integration Tests
  runs-on: ubuntu-latest
  services:
    scylladb:
      image: scylladb/scylla:latest
      ports:
        - 9042:9042
        - 8080:8080
      options: >-
        --health-cmd "cqlsh -e 'SELECT now() FROM system.local'"
        --health-interval 10s
        --health-timeout 5s
        --health-retries 10
  steps:
    - uses: actions/checkout@v4
    - uses: astral-sh/setup-uv@v6
    - run: uv sync --dev
    - run: uv run pytest tests/integration/
```

## Trigger Patterns

### Standard CI

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
```

### Post-CI Analysis

```yaml
on:
  workflow_run:
    workflows: ["CI"]
    types: [completed]
```

### Matrix Builds

```yaml
strategy:
  fail-fast: false
  matrix:
    python-version: ["3.11", "3.12", "3.13"]
    os: [ubuntu-latest, macos-latest]
```

## Debugging Workflows

### Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| `Permission denied` on PR comment | Missing `pull-requests: write` | Add to `permissions:` |
| uv install fails | Cache stale | Clear cache or update lock |
| ScyllaDB service not ready | Health check too fast | Increase retries |

### Viewing Logs

```bash
gh run view <run-id> --log-failed
gh run list --workflow ci.yml --limit 5
gh run rerun <run-id> --failed
```

## Validation Checklist

- [ ] Workflow YAML is valid
- [ ] All jobs have `name:` for readable UI
- [ ] Permissions follow least privilege
- [ ] uv caching is configured
- [ ] Artifacts have appropriate `retention-days`
- [ ] `if: always()` used for artifact uploads
- [ ] Secrets are not logged

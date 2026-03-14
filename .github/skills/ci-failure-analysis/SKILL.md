---
name: ci-failure-analysis
description: >-
  Implement and configure AI-powered CI failure analysis workflows for GitHub
  Actions. Use when setting up CI failure summaries, configuring claude-code-action
  for failure diagnosis, writing workflow_run triggered analysis, creating
  collapsed PR comments with failure diagnostics, implementing flaky test
  detection, or working on recurring issue tracking.
---

# CI Failure Analysis

Implement AI-powered CI failure analysis that automatically diagnoses failing CI jobs and posts structured, collapsed PR comments with root cause analysis, fix suggestions, and recurring issue detection.

## Before Starting

1. Read `docs/plans/03-testing-strategy.md` — the testing strategy plan
2. Read any existing CI workflow in `.github/workflows/`
3. Check `docs/plans/high-level-design.md` for project context

## Architecture

The system has three components:

1. **Test output collection** — `pytest` produces JUnit XML for structured test data
2. **Failure analysis workflow** — `ci-failure-analysis.yml` triggers on `workflow_run` completion, invokes `anthropics/claude-code-action` to analyze logs
3. **PR comment posting** — `actions/github-script` formats and posts/updates a collapsed comment

```
CI Workflow Fails
    ├─> Collect JUnit XML (pytest --junitxml)
    ├─> Collect raw logs (gh run view --log-failed)
    ├─> Invoke claude-code-action with JSON schema
    │     ├─> Classify each failure
    │     ├─> Identify root cause
    │     ├─> Suggest fixes (file:line references)
    │     └─> Detect flaky tests
    ├─> Post/update collapsed PR comment
    └─> Auto-retry if flaky (confidence > 0.8)
```

## Key Implementation Details

### Workflow Trigger

Use `workflow_run` to trigger analysis after the CI workflow completes:

```yaml
on:
  workflow_run:
    workflows: ["CI"]
    types: [completed]

jobs:
  analyze-failure:
    if: >
      github.event.workflow_run.conclusion == 'failure' &&
      github.event.workflow_run.event == 'pull_request'
```

### Required Permissions

```yaml
permissions:
  contents: read
  pull-requests: write
  actions: read
  checks: read
  id-token: write
```

### Failure Classification Taxonomy

| Category | Description | Auto-action |
|----------|-------------|-------------|
| `test_failure` | Test assertion failed | None |
| `lint_violation` | ruff or formatting failure | Suggest exact fix |
| `import_error` | Missing or broken import | Suggest `uv sync` |
| `infrastructure_flaky` | Timeout, container startup, network | Auto-retry if confidence > 0.8 |
| `dependency_issue` | Package resolution, version conflict | Suggest `uv sync` |
| `configuration_error` | CI YAML issue, missing secret | Link to docs |
| `unknown` | Cannot classify | Flag for manual review |

### PR Comment Format

Use GitHub `<details>` tags for collapsible sections. Structure:

1. **Summary header** — pass/fail counts, classification labels
2. **Failed job sections** (collapsed) — one `<details>` per failed job
3. **Recurring issues section** (collapsed) — patterns across runs
4. **Footer** — re-run link, attribution

### Comment Deduplication

Always check for an existing bot comment starting with `## CI Failure Summary` and update it rather than creating a duplicate.

### pytest JUnit XML Setup

```yaml
- run: uv run pytest --junitxml=test-results.xml
- uses: actions/upload-artifact@v4
  if: always()
  with:
    name: test-results
    path: test-results.xml
```

## Validation Checklist

- [ ] CI failures trigger the analysis workflow
- [ ] PR comment appears with collapsed sections
- [ ] Each failure has: error message, root cause, suggested fix, classification
- [ ] Comment is updated (not duplicated) on subsequent pushes
- [ ] Recurring issues are detected across runs
- [ ] Flaky tests are auto-retried when detected

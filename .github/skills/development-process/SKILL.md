---
name: development-process
description: >-
  Guide the end-to-end development process for hydra-locust features: review
  plans, design tests, implement code, write tests, and update plan documents.
  Use when starting a new feature, picking up the next development task, or
  following the project's development workflow from plan to implementation.
---

# Development Process

Guide the structured development process for hydra-locust, from plan review through implementation, testing, and documentation updates.

## Workflow Overview

```
1. Review Plans  →  2. Design Tests  →  3. Implement  →  4. Test  →  5. Update Plans  →  6. Update Docs  →  7. Commit
```

Each feature follows this deterministic workflow. Never skip steps.

## Step 1: Review Plans

1. Read the master plan: `docs/plans/high-level-design.md`
2. Identify the next incomplete sub-plan (SP1–SP11) based on phase order
3. Read the target sub-plan fully
4. Read `docs/plans/03-testing-strategy.md` for testing requirements
5. Identify dependencies on other sub-plans

### Picking the Next Task

- Follow phase order: Phase 1 → Phase 2 → Phase 3 → Phase 4
- Within a phase, prioritize tasks marked ☐ TODO before new work
- Check acceptance criteria of predecessor tasks — they must be met first
- If a sub-plan has status "IN PROGRESS", continue it; if "DONE", skip it

## Step 2: Design Tests

Before writing implementation code, design the test strategy:

1. **Unit tests** — Identify every public function and its edge cases
2. **Integration tests** — Identify interactions that need containers
3. **Smoke tests** — Verify basic functionality works end-to-end

### Test Design Checklist

- [ ] Happy path for each feature
- [ ] Edge cases (empty input, maximum values, Unicode, special characters)
- [ ] Error cases (invalid input, missing files, connection failures)
- [ ] gevent compatibility (if applicable)

## Step 3: Implement

### Module Structure

Follow the established layout:

```
hydra-locust/
├── common.py               # Shared utilities
├── locustfile.py           # CQL workloads
├── dynamodb_case1.py       # DynamoDB workloads
├── prom_collector.py       # Prometheus metrics
├── benchmark.py            # Sync benchmarks
├── benchmark_asynio.py     # Async benchmarks
├── tests/
│   ├── __init__.py
│   ├── test_common.py      # Unit tests for common.py
│   └── ...                 # Additional test files
├── docs/plans/             # Design documents
└── pyproject.toml
```

### Implementation Checklist

- [ ] Read existing code in the module area before making changes
- [ ] Follow the relevant sub-plan tasks
- [ ] Use type hints for public functions
- [ ] Add or update tests
- [ ] Maintain gevent compatibility where needed
- [ ] Use `report_timings` decorator for Locust integration

### Code Conventions

- **Error handling**: Use explicit exception handling, log errors
- **Concurrency**: gevent for Locust, asyncio for standalone benchmarks
- **Configuration**: CLI args via Locust, environment variables for Docker
- **Imports**: Group stdlib → third-party → local, use ruff for sorting

## Step 4: Test

### Running Tests

```bash
# Install dev dependencies
uv sync --dev

# Run linter
uv run ruff check .

# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_common.py

# Run with verbose output
uv run pytest -v

# Run with output capture disabled (for debugging)
uv run pytest -s
```

### Test Quality Gates

- All tests must pass before committing
- No `@pytest.mark.skip` without a tracking issue
- Unit tests must cover happy path, edge cases, and error cases

## Step 5: Update Plans

After implementation, update the sub-plan document:

1. Mark completed steps with ✅
2. Update status line at the top
3. Record key decisions with rationale
4. Remove speculative options that were not chosen

### Plan Update Template

```markdown
> **Status: IN PROGRESS** — [description] ([date])
```

or

```markdown
> **Status: DONE** — Completed [date], PR #XX
```

## Step 6: Update Documentation

After implementation and plan updates, review whether user-facing documentation needs changes.

### When to Update README.md

- New CLI flags or arguments
- New environment variables
- New configuration options
- New features or workload types
- Changed defaults
- New dependencies

### What NOT to Update

- Internal refactoring
- Test-only changes
- Plan/design document updates

## Step 7: Commit

Use the conventional-commit skill or follow this format:

```
type(scope): short description

Longer description of what was done and why.

- Key point 1
- Key point 2
```

### Commit Strategy

- **Separate commits** for code vs plan updates vs docs
- **Code commit**: `feat(scope):` or `fix(scope):`
- **Plan commit**: `docs(plan):`
- **Docs commit**: `docs:`
- Never mix code changes with documentation changes in one commit

## Dependencies

| Package | Purpose | Version |
|---------|---------|---------|
| `locust` | Load testing framework | >=2.43 |
| `numpy` | Zipfian distribution | >=2.4 |
| `prometheus-client` | Metrics export | >=0.24 |
| `scylla-driver` | CQL driver | >=3.29 |
| `aioboto3` | Async DynamoDB | >=15.5 |
| `pytest` | Testing | >=9.0 (dev) |
| `ruff` | Linting | >=0.15 (dev) |

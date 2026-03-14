# Sub-Plan SP1: Modernize the Code

> Parent: [high-level-design.md](high-level-design.md) | Phase 1
>
> **Status: IN PROGRESS** — pyproject.toml and uv migration complete (2026-03-14)
>
> **This is a living document.** Update it as development progresses.

## Objective

Modernize the project's build system, dependency management, and documentation to align with current Python ecosystem best practices, enabling easier contribution and maintenance.

---

## Requirements & Constraints

| ID | Type | Description |
|----|------|-------------|
| REQ-01 | Requirement | Use `pyproject.toml` as the single source of project metadata |
| REQ-02 | Requirement | Use `uv` as the package manager with a lock file |
| REQ-03 | Requirement | Pin minimum Python version to 3.11+ |
| REQ-04 | Requirement | All dependencies must be up to date |
| REQ-05 | Requirement | README must document uv-based workflow |
| CON-01 | Constraint | Must not break existing Docker builds |
| CON-02 | Constraint | Must maintain compatibility with Locust's gevent model |

## Design Decisions

| Decision | Choice | Rationale | Alternatives Rejected |
|----------|--------|-----------|----------------------|
| Package manager | `uv` | Fastest Python package manager, supports lock files | pip-tools, poetry, pdm |
| Project metadata | `pyproject.toml` | PEP 621 standard, single source of truth | setup.py, setup.cfg |
| Linter | `ruff` | Fast, replaces flake8 + isort + pyupgrade | flake8, pylint |
| Python version | 3.11+ | f-string improvements, tomllib, typing improvements | 3.10, 3.12 |

## Implementation Tasks

### Phase 1.1: Build System Migration

| # | Task | Description | Validation | Status |
|---|------|-------------|------------|--------|
| 1.1.1 | Create `pyproject.toml` | Define project metadata, dependencies, tool configs | `uv sync` succeeds | ✅ Done |
| 1.1.2 | Create `uv.lock` | Generate lock file for reproducible installs | `uv sync --frozen` succeeds | ✅ Done |
| 1.1.3 | Remove legacy files | Delete `requirements.in`, `requirements.txt` | Files removed | ✅ Done |
| 1.1.4 | Update `.gitignore` | Add uv-specific patterns | Patterns present | ✅ Done |

### Phase 1.2: Dependency Updates

| # | Task | Description | Validation | Status |
|---|------|-------------|------------|--------|
| 1.2.1 | Upgrade `scylla-driver` | Update to latest release | `uv run python -c "import cassandra"` works | ✅ Done |
| 1.2.2 | Upgrade all dependencies | Update locust, boto3, aioboto3, numpy, prometheus-client | `uv sync` with latest versions | ✅ Done |
| 1.2.3 | Set up automated updates | Configure Dependabot or Renovate | PR bot active | ☐ TODO |

### Phase 1.3: Documentation

| # | Task | Description | Validation | Status |
|---|------|-------------|------------|--------|
| 1.3.1 | Update `README.md` | Rewrite for uv-based workflow | Install instructions work | ✅ Done |
| 1.3.2 | Add architecture docs | Create `docs/` site with MkDocs or Sphinx | Docs build | ☐ TODO |
| 1.3.3 | Add contributing guide | Document development workflow | Guide exists | ☐ TODO |

### Phase 1.4: Docker

| # | Task | Description | Validation | Status |
|---|------|-------------|------------|--------|
| 1.4.1 | Update Dockerfile | Use uv in Docker build | `docker build .` succeeds | ✅ Done |
| 1.4.2 | Update `.dockerignore` | Ensure only needed files are included | Build context is minimal | ✅ Done |

---

## Testing Strategy

| ID | Test Type | Description | Validation |
|----|-----------|-------------|------------|
| TEST-01 | Smoke | `uv sync && uv run python -c "import common"` | Imports succeed |
| TEST-02 | Lint | `uv run ruff check .` | No errors |
| TEST-03 | Unit | `uv run pytest` | All tests pass |
| TEST-04 | Docker | `docker build .` | Image builds |

## Risks

| ID | Risk | Mitigation |
|----|------|-----------|
| RISK-01 | uv is relatively new tool | uv has strong community adoption; pip fallback documented |
| RISK-02 | scylla-driver breaking changes | Pin to known-good version, test before upgrading |

# Hydra-Locust — High-Level Design

> **This is a living document.** Update it as development progresses.

## Project Overview

Hydra-Locust is a Locust-based CQL/DynamoDB load testing tool for ScyllaDB, Cassandra, and DynamoDB-compatible databases. It provides high-performance workload generation with Zipfian key distributions, timing decorators for Locust event integration, Prometheus metrics export, and multi-process worker support.

## Architecture

- **Language**: Python 3.11+
- **Package Manager**: uv
- **Load Framework**: Locust
- **CQL Driver**: scylla-driver (cassandra-driver fork)
- **DynamoDB Driver**: boto3 / aioboto3
- **Metrics**: prometheus-client
- **Distribution**: numpy (Zipfian)
- **Linting**: ruff
- **Testing**: pytest

## Project Structure

```
hydra-locust/
├── docs/
│   └── plans/              # Design documents and sub-plans
│       ├── high-level-design.md   # This file — master plan
│       ├── 01-modernize-code.md
│       ├── 02-skill-system.md
│       ├── 03-testing-strategy.md
│       ├── 04-pluggable-drivers.md
│       ├── 05-coodie-support.md
│       ├── 06-latte-features.md
│       ├── 07-performance-review.md
│       ├── 08-script-conversion.md
│       ├── 09-hdr-histograms.md
│       ├── 10-prometheus-support.md
│       └── 11-unified-cli.md
├── tests/
│   ├── __init__.py
│   └── test_common.py
├── .github/
│   ├── copilot-instructions.md
│   ├── instructions/
│   │   └── memory.instructions.md
│   └── skills/               # AI assistant skills
│       ├── ci-failure-analysis/
│       ├── conventional-commit/
│       ├── create-implementation-plan/
│       ├── development-process/
│       ├── github-actions/
│       ├── remember/
│       └── skill-creator/
├── common.py               # Shared utilities (timing, distributions, workers)
├── locustfile.py           # CQL/Cassandra workload
├── dynamodb_case1.py       # DynamoDB/Alternator workload
├── prom_collector.py       # Prometheus metrics exporter
├── benchmark.py            # Sync DynamoDB benchmark
├── benchmark_asynio.py     # Async DynamoDB benchmark
├── pyproject.toml
├── uv.lock
├── Dockerfile
└── README.md
```

## Phased Implementation

### Phase 1: Foundation (Modernize & Test)

| Sub-Plan | Title | Status |
|----------|-------|--------|
| [SP1](01-modernize-code.md) | Modernize the Code | IN PROGRESS |
| [SP3](03-testing-strategy.md) | Testing Strategy | IN PROGRESS |

### Phase 2: Skill System & Drivers

| Sub-Plan | Title | Status |
|----------|-------|--------|
| [SP2](02-skill-system.md) | Skill System | NOT STARTED |
| [SP4](04-pluggable-drivers.md) | Pluggable Drivers | NOT STARTED |
| [SP5](05-coodie-support.md) | Coodie Support | NOT STARTED |

### Phase 3: Advanced Features

| Sub-Plan | Title | Status |
|----------|-------|--------|
| [SP6](06-latte-features.md) | Latte-like Features | NOT STARTED |
| [SP7](07-performance-review.md) | Performance Review | NOT STARTED |
| [SP8](08-script-conversion.md) | Script Conversion | NOT STARTED |

### Phase 4: Observability & Integration

| Sub-Plan | Title | Status |
|----------|-------|--------|
| [SP9](09-hdr-histograms.md) | HDR Histograms | NOT STARTED |
| [SP10](10-prometheus-support.md) | Prometheus Support | IN PROGRESS |
| [SP11](11-unified-cli.md) | Unified CLI | NOT STARTED |

---

## Key Conventions

- All design documents live in `docs/plans/`
- This document is the master plan — read it before making architectural decisions
- Plans are living documents: update them when decisions are made
- Use Conventional Commits for all commit messages
- Follow `ruff` formatting and linting rules
- All tests use `pytest`

## Code Style

- Follow `ruff` defaults (line length 120, Python 3.11 target)
- Use type hints for all public functions
- Use `gevent` monkey-patching for Locust compatibility
- Use decorators (`report_timings`) for consistent Locust event reporting
- Prefer composition over inheritance for workload patterns

## Testing

- Unit tests: `tests/` directory using `pytest`
- Integration tests: Against ScyllaDB/Cassandra/DynamoDB containers
- Benchmarks: `benchmark.py` and `benchmark_asynio.py` for driver performance
- Run tests: `uv run pytest`
- Run linter: `uv run ruff check .`

## Dependencies

| Package | Purpose | Version |
|---------|---------|---------|
| `locust` | Load testing framework | >=2.43 |
| `numpy` | Zipfian distribution | >=2.4 |
| `prometheus-client` | Metrics export | >=0.24 |
| `scylla-driver` | CQL driver (Cassandra/ScyllaDB) | >=3.29 |
| `aioboto3` | Async DynamoDB driver | >=15.5 |
| `pytest` | Testing framework | >=9.0 (dev) |
| `ruff` | Linter and formatter | >=0.15 (dev) |

## Completed Work

- [x] Migrated to `pyproject.toml` + `uv` package manager
- [x] Pinned Python 3.11+ minimum version
- [x] Implemented CQL workload (`locustfile.py`)
- [x] Implemented DynamoDB workload (`dynamodb_case1.py`)
- [x] Implemented Prometheus metrics exporter (`prom_collector.py`)
- [x] Added unit tests for `common.py` utilities
- [x] Configured `ruff` for linting
- [x] Created `Dockerfile` for containerized deployment

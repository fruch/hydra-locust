# hydra-locust — Copilot Instructions

## Project Overview

hydra-locust is a Locust-based CQL/DynamoDB load testing tool for ScyllaDB, Cassandra, and DynamoDB-compatible databases. It provides high-performance workload generation with Zipfian key distributions, timing decorators for Locust event integration, Prometheus metrics export, and multi-process worker support.

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

## Key Conventions

- All design documents live in `docs/plans/`
- The master plan is `docs/plans/high-level-design.md` — read it before making architectural decisions
- Plans are living documents: update them when decisions are made
- Use Conventional Commits for all commit messages
- Every feature should reference the relevant sub-plan

## Code Style

- Follow `ruff` defaults (line length 120, Python 3.11 target)
- Use type hints for all public functions
- Use `gevent` monkey-patching for Locust compatibility
- Use decorators (`report_timings`) for consistent Locust event reporting
- Prefer composition over inheritance for workload patterns

## Testing

- Unit tests: `tests/` directory using `pytest`
- Integration tests: Against ScyllaDB/Cassandra/DynamoDB containers
- Run tests: `uv run pytest`
- Run linter: `uv run ruff check .`
- Install dev dependencies: `uv sync --dev`

# Sub-Plan SP3: Testing Strategy

> Parent: [high-level-design.md](high-level-design.md) | Phase 1
>
> **Status: IN PROGRESS** — Unit tests for common.py complete (2026-03-14)
>
> **This is a living document.** Update it as development progresses.

## Objective

Establish a comprehensive testing strategy covering unit tests, integration tests, and benchmarks to ensure correctness, prevent regressions, and track performance over time.

---

## Requirements & Constraints

| ID | Type | Description |
|----|------|-------------|
| REQ-01 | Requirement | Unit tests for all utility functions in `common.py` |
| REQ-02 | Requirement | Integration tests against ScyllaDB/Cassandra containers |
| REQ-03 | Requirement | Integration tests against DynamoDB-compatible containers |
| REQ-04 | Requirement | Reproducible benchmarks for driver layer |
| REQ-05 | Requirement | CI integration via GitHub Actions |
| CON-01 | Constraint | Tests must work with `uv run pytest` |
| CON-02 | Constraint | Integration tests require Docker |

## Design Decisions

| Decision | Choice | Rationale | Alternatives Rejected |
|----------|--------|-----------|----------------------|
| Test framework | `pytest` | Standard Python testing, rich plugin ecosystem | unittest, nose |
| Container management | `testcontainers-python` or docker-compose | Programmatic container lifecycle | Manual setup |
| Benchmark approach | `pytest-benchmark` or custom scripts | Integrates with existing test runner | Separate benchmark tool |

## Implementation Tasks

### Phase 3.1: Unit Tests

| # | Task | Description | Validation | Status |
|---|------|-------------|------------|--------|
| 3.1.1 | Test `iter_shuffle` | All elements produced, reordering verified | 6 tests pass | ✅ Done |
| 3.1.2 | Test `iter_zipf` | Range, distribution skew, infinite generation | 3 tests pass | ✅ Done |
| 3.1.3 | Test `report_timings` | Success/failure events, elapsed time, aliases | 7 tests pass | ✅ Done |
| 3.1.4 | Test skill system | Skill loading, composition, configuration | Tests pass | ☐ TODO |
| 3.1.5 | Test Prometheus collector | Metric collection and formatting | Tests pass | ☐ TODO |

### Phase 3.2: Integration Tests

| # | Task | Description | Validation |
|---|------|-------------|------------|
| 3.2.1 | ScyllaDB container setup | Start ScyllaDB in CI for CQL tests | Container starts and accepts connections |
| 3.2.2 | CQL workload integration test | Run `locustfile.py` against ScyllaDB | Workload completes without errors |
| 3.2.3 | DynamoDB container setup | Start Alternator or DynamoDB Local | Container starts and accepts connections |
| 3.2.4 | DynamoDB workload integration test | Run `dynamodb_case1.py` against container | Workload completes without errors |

### Phase 3.3: Benchmarks

| # | Task | Description | Validation |
|---|------|-------------|------------|
| 3.3.1 | Driver micro-benchmarks | Measure raw driver throughput | Benchmark results reproducible |
| 3.3.2 | Data generation benchmarks | Benchmark Zipfian and shuffle generators | Results within expected range |
| 3.3.3 | Regression tracking | Compare benchmark results across commits | Regressions detected |

### Phase 3.4: CI Integration

| # | Task | Description | Validation |
|---|------|-------------|------------|
| 3.4.1 | GitHub Actions workflow | Run lint + unit tests on every PR | Workflow passes |
| 3.4.2 | Integration test workflow | Run integration tests on merge to main | Workflow passes |
| 3.4.3 | Benchmark workflow | Run benchmarks on demand or weekly | Results published |

---

## Coverage Targets

| Module | Target |
|--------|--------|
| `common.py` | >90% |
| Skill system | >85% |
| `prom_collector.py` | >80% |
| Workload files | >70% (integration) |

## Testing Strategy

| ID | Test Type | Description | Validation |
|----|-----------|-------------|------------|
| TEST-01 | Unit | `common.py` utilities | `uv run pytest tests/test_common.py` passes |
| TEST-02 | Integration | CQL workload end-to-end | Workload runs against container |
| TEST-03 | Integration | DynamoDB workload end-to-end | Workload runs against container |
| TEST-04 | Benchmark | Driver throughput | Results within expected range |

## Risks

| ID | Risk | Mitigation |
|----|------|-----------|
| RISK-01 | Container startup time in CI | Use health checks and retry logic |
| RISK-02 | Flaky integration tests | Implement retry mechanism, detect flaky tests |
| RISK-03 | Benchmark noise in CI | Run on dedicated hardware or use statistical analysis |

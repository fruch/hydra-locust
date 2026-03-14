# Sub-Plan SP5: Coodie Support

> Parent: [high-level-design.md](high-level-design.md) | Phase 2
>
> **Status: NOT STARTED**
>
> **This is a living document.** Update it as development progresses.

## Objective

Implement a [coodie](https://github.com/fruch/coodie) (Rust-based CQL driver) adapter for hydra-locust, enabling shard-aware routing and benchmarking coodie vs. scylla-driver under identical workloads.

---

## Requirements & Constraints

| ID | Type | Description |
|----|------|-------------|
| REQ-01 | Requirement | Implement coodie as a pluggable CQL driver |
| REQ-02 | Requirement | Provide example workloads exercising coodie-specific features |
| REQ-03 | Requirement | Benchmark coodie vs. scylla-driver under identical conditions |
| REQ-04 | Requirement | Document setup, installation, and usage |
| CON-01 | Constraint | Depends on SP4 (Pluggable Drivers) being complete |
| CON-02 | Constraint | coodie must be installable via pip (Python bindings) |

## Design Decisions

| Decision | Choice | Rationale | Alternatives Rejected |
|----------|--------|-----------|----------------------|
| Integration method | Python bindings via PyO3 | Native speed with Python API | subprocess, FFI |

## Implementation Tasks

### Phase 5.1: Driver Adapter

| # | Task | Description | Validation |
|---|------|-------------|------------|
| 5.1.1 | Implement `CoodieDriver` | Adapt coodie Python bindings to `CQLDriver` protocol | Protocol conformance test passes |
| 5.1.2 | Shard-aware routing support | Leverage coodie's shard-aware routing | Routing verified in tests |
| 5.1.3 | Connection pooling | Map coodie's pool to hydra-locust expectations | Connections reused |

### Phase 5.2: Workloads & Benchmarks

| # | Task | Description | Validation |
|---|------|-------------|------------|
| 5.2.1 | Example workload | Locust workload using coodie driver | Workload runs end-to-end |
| 5.2.2 | Comparative benchmark | Same workload with scylla-driver vs. coodie | Results published |
| 5.2.3 | Shard-aware benchmark | Benchmark shard-aware vs. non-shard-aware | Improvement measured |

### Phase 5.3: Documentation

| # | Task | Description | Validation |
|---|------|-------------|------------|
| 5.3.1 | Installation guide | How to install coodie for use with hydra-locust | Guide works |
| 5.3.2 | Usage guide | How to select and configure coodie driver | Guide works |
| 5.3.3 | Benchmark report | Publish comparison results | Report complete |

---

## Dependencies

| ID | Dependency | Required By |
|----|-----------|-------------|
| DEP-01 | SP4 (Pluggable Drivers) | All tasks |
| DEP-02 | coodie Python bindings | Task 5.1.1 |

## Testing Strategy

| ID | Test Type | Description | Validation |
|----|-----------|-------------|------------|
| TEST-01 | Unit | CoodieDriver protocol conformance | Mock tests pass |
| TEST-02 | Integration | coodie workload against ScyllaDB | Workload completes |
| TEST-03 | Benchmark | coodie vs. scylla-driver | Results reproducible |

## Risks

| ID | Risk | Mitigation |
|----|------|-----------|
| RISK-01 | coodie Python bindings not mature | Track coodie releases, contribute upstream |
| RISK-02 | gevent incompatibility with Rust bindings | Test early, consider async alternative |

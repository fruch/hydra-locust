# Sub-Plan SP11: Unified CLI Frontend

> Parent: [high-level-design.md](high-level-design.md) | Phase 4
>
> **Status: NOT STARTED**
>
> **This is a living document.** Update it as development progresses.

## Objective

Provide a unified CLI frontend that can drive multiple stress testing backends (latte, cassandra-stress, scylla-bench, YCSB) through a single, consistent command-line interface with common flags and result aggregation.

---

## Requirements & Constraints

| ID | Type | Description |
|----|------|-------------|
| REQ-01 | Requirement | Common flags for connection, duration, concurrency, output |
| REQ-02 | Requirement | Translate common CLI to each tool's native arguments |
| REQ-03 | Requirement | Aggregate and normalize results from all backends |
| REQ-04 | Requirement | Support running multiple backends in parallel |
| CON-01 | Constraint | Backend tools must be installed separately |
| CON-02 | Constraint | Must not modify backend tool behavior |

## Supported Backends

| Backend | Description | Native CLI |
|---------|-------------|-----------|
| **latte** | Rune-based Cassandra stress tool | `latte run` |
| **cassandra-stress** | Built-in Cassandra stress utility | `cassandra-stress` |
| **scylla-bench** | Go-based Scylla benchmark tool | `scylla-bench` |
| **YCSB** | Yahoo! Cloud Serving Benchmark | `ycsb run` |

## Design Decisions

| Decision | Choice | Rationale | Alternatives Rejected |
|----------|--------|-----------|----------------------|
| CLI framework | `click` or `argparse` | Subcommand support, Python standard | typer (extra dependency) |
| Result format | JSON with normalized schema | Machine-readable, composable | CSV, custom binary |
| Backend integration | subprocess with argument translation | Simple, no backend modification | SDK/API integration |

## Implementation Tasks

### Phase 11.1: Core CLI

| # | Task | Description | Validation |
|---|------|-------------|------------|
| 11.1.1 | CLI framework | Set up `hydra-locust` CLI with subcommands | `hydra-locust --help` works |
| 11.1.2 | Common flags | `--host`, `--duration`, `--concurrency`, `--output` | Flags accepted |
| 11.1.3 | Backend registry | Register and discover available backends | Backends listed |

### Phase 11.2: Backend Adapters

| # | Task | Description | Validation |
|---|------|-------------|------------|
| 11.2.1 | latte adapter | Translate common flags to `latte run` args | latte runs |
| 11.2.2 | cassandra-stress adapter | Translate to `cassandra-stress` args | Tool runs |
| 11.2.3 | scylla-bench adapter | Translate to `scylla-bench` args | Tool runs |
| 11.2.4 | YCSB adapter | Translate to `ycsb run` args | Tool runs |

### Phase 11.3: Result Aggregation

| # | Task | Description | Validation |
|---|------|-------------|------------|
| 11.3.1 | Result parser per backend | Parse each tool's output format | Results parsed |
| 11.3.2 | Normalized schema | Common JSON schema for all results | Schema validates |
| 11.3.3 | Comparison report | Side-by-side comparison of backends | Report generated |
| 11.3.4 | Parallel execution | Run multiple backends simultaneously | Results from all backends |

---

## Dependencies

| ID | Dependency | Required By |
|----|-----------|-------------|
| DEP-01 | SP1 (Modernize Code) | All tasks |
| DEP-02 | Backend tools installed | Phase 11.2 |

## Testing Strategy

| ID | Test Type | Description | Validation |
|----|-----------|-------------|------------|
| TEST-01 | Unit | Flag translation per backend | Arguments correct |
| TEST-02 | Unit | Result parsing per backend | Results parsed |
| TEST-03 | Integration | Full run with mock backend | End-to-end works |

## Risks

| ID | Risk | Mitigation |
|----|------|-----------|
| RISK-01 | Backend CLI changes between versions | Pin supported versions, document compatibility |
| RISK-02 | Result format parsing fragile | Use structured output (JSON) where available |
| RISK-03 | Cross-platform compatibility | Test on Linux, macOS |

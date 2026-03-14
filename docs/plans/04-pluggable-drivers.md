# Sub-Plan SP4: Pluggable Drivers

> Parent: [high-level-design.md](high-level-design.md) | Phase 2
>
> **Status: NOT STARTED**
>
> **This is a living document.** Update it as development progresses.

## Objective

Refactor the driver layer behind a common interface so that CQL and DynamoDB drivers are pluggable, allowing third-party drivers (including Rust-based coodie) to be used transparently.

---

## Requirements & Constraints

| ID | Type | Description |
|----|------|-------------|
| REQ-01 | Requirement | Define a minimal driver contract: connect, prepare, execute, close |
| REQ-02 | Requirement | Support driver selection via configuration or CLI flag |
| REQ-03 | Requirement | scylla-driver must work as the default CQL driver |
| REQ-04 | Requirement | boto3/aioboto3 must work as the default DynamoDB driver |
| REQ-05 | Requirement | Third-party drivers can be plugged in via Python interface |
| CON-01 | Constraint | Must work with gevent monkey-patching |
| CON-02 | Constraint | Must integrate with Locust timing decorators |

## Design Decisions

| Decision | Choice | Rationale | Alternatives Rejected |
|----------|--------|-----------|----------------------|
| Interface | Python Protocol (PEP 544) | Structural typing, no inheritance required | ABC, duck typing |
| Driver selection | `--driver` CLI flag + config | Explicit selection, easy to understand | Auto-detection |

## Implementation Tasks

### Phase 4.1: Driver Interface

| # | Task | Description | Validation |
|---|------|-------------|------------|
| 4.1.1 | Define `CQLDriver` protocol | Protocol class with connect, prepare, execute, close | Protocol importable |
| 4.1.2 | Define `DynamoDBDriver` protocol | Protocol class for DynamoDB operations | Protocol importable |
| 4.1.3 | Implement scylla-driver adapter | Wrap scylla-driver behind `CQLDriver` | Existing workloads work |
| 4.1.4 | Implement boto3 adapter | Wrap boto3 behind `DynamoDBDriver` | Existing workloads work |

### Phase 4.2: Driver Selection

| # | Task | Description | Validation |
|---|------|-------------|------------|
| 4.2.1 | Add `--driver` CLI flag | Allow selecting driver by name | Flag accepted |
| 4.2.2 | Implement driver registry | Map driver names to implementations | Registry resolves drivers |
| 4.2.3 | Add driver config section | YAML/TOML config for driver parameters | Config loads |

### Phase 4.3: Documentation

| # | Task | Description | Validation |
|---|------|-------------|------------|
| 4.3.1 | Driver interface docs | Document the protocol classes | Docs complete |
| 4.3.2 | Third-party driver guide | How to implement a custom driver | Guide complete |

---

## Dependencies

| ID | Dependency | Required By |
|----|-----------|-------------|
| DEP-01 | SP1 (Modernize Code) | All tasks |

## Testing Strategy

| ID | Test Type | Description | Validation |
|----|-----------|-------------|------------|
| TEST-01 | Unit | Protocol conformance tests | Mock drivers pass |
| TEST-02 | Integration | scylla-driver adapter | CQL workload works |
| TEST-03 | Integration | boto3 adapter | DynamoDB workload works |

## Risks

| ID | Risk | Mitigation |
|----|------|-----------|
| RISK-01 | Interface too restrictive for some drivers | Start minimal, extend based on need |
| RISK-02 | Performance overhead from abstraction | Benchmark adapter vs. direct usage |

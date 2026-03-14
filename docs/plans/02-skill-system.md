# Sub-Plan SP2: Skill System

> Parent: [high-level-design.md](high-level-design.md) | Phase 2
>
> **Status: NOT STARTED**
>
> **This is a living document.** Update it as development progresses.

## Objective

Design and implement a skill abstraction that encapsulates reusable workload patterns (read-heavy, write-heavy, mixed, scan, batch), allowing declarative composition and external extensibility.

---

## Requirements & Constraints

| ID | Type | Description |
|----|------|-------------|
| REQ-01 | Requirement | Skills must be composable via YAML/TOML configuration |
| REQ-02 | Requirement | Skills must also be usable via Python API |
| REQ-03 | Requirement | Ship built-in skills for common CQL and DynamoDB workloads |
| REQ-04 | Requirement | Support user-defined skills from external modules |
| REQ-05 | Requirement | Skills must integrate with Locust's event system |
| CON-01 | Constraint | Must work with gevent-based concurrency model |
| CON-02 | Constraint | Must not break existing locustfile.py usage |

## Design Decisions

| Decision | Choice | Rationale | Alternatives Rejected |
|----------|--------|-----------|----------------------|
| Skill definition | Python classes with YAML config | Flexible, familiar to Python users | Pure YAML, plugin registry |
| Configuration format | YAML | Human-readable, widely supported | TOML (less flexible for nested config) |
| Skill discovery | Entry points + module paths | Standard Python extension mechanism | File-system scanning |

## Implementation Tasks

### Phase 2.1: Core Abstraction

| # | Task | Description | Validation |
|---|------|-------------|------------|
| 2.1.1 | Define `Skill` base class | Abstract base class with `setup()`, `execute()`, `teardown()` | Class importable |
| 2.1.2 | Define skill configuration schema | YAML schema for skill parameters | Schema validates |
| 2.1.3 | Implement skill registry | Discovery and loading of skills | Registry loads built-ins |
| 2.1.4 | Implement skill composition | Combine multiple skills with weights | Composed skill runs |

### Phase 2.2: Built-in Skills

| # | Task | Description | Validation |
|---|------|-------------|------------|
| 2.2.1 | CQL read-heavy skill | 80% reads, 20% writes | Runs against ScyllaDB |
| 2.2.2 | CQL write-heavy skill | 80% writes, 20% reads | Runs against ScyllaDB |
| 2.2.3 | CQL mixed skill | 50/50 reads and writes | Runs against ScyllaDB |
| 2.2.4 | DynamoDB read-heavy skill | 80% reads, 20% writes | Runs against Alternator |
| 2.2.5 | DynamoDB write-heavy skill | 80% writes, 20% reads | Runs against Alternator |
| 2.2.6 | CQL scan skill | Full table scan pattern | Runs against ScyllaDB |
| 2.2.7 | CQL batch skill | Batch insert pattern | Runs against ScyllaDB |

### Phase 2.3: External Skills

| # | Task | Description | Validation |
|---|------|-------------|------------|
| 2.3.1 | External module loading | Load skills from user-specified modules | Custom skill runs |
| 2.3.2 | Entry point discovery | Discover skills via `entry_points` | Installed skill discovered |
| 2.3.3 | Skill documentation | Document how to create custom skills | Guide complete |

---

## Dependencies

| ID | Dependency | Required By |
|----|-----------|-------------|
| DEP-01 | SP1 (Modernize Code) | All tasks |
| DEP-02 | SP4 (Pluggable Drivers) | Driver-agnostic skills |

## Testing Strategy

| ID | Test Type | Description | Validation |
|----|-----------|-------------|------------|
| TEST-01 | Unit | Skill base class and registry | `uv run pytest tests/test_skills.py` |
| TEST-02 | Unit | YAML configuration parsing | Config loads and validates |
| TEST-03 | Integration | Built-in skills against containers | Skills complete workload |
| TEST-04 | Integration | External skill loading | Custom skill discovered and runs |

## Risks

| ID | Risk | Mitigation |
|----|------|-----------|
| RISK-01 | Skill abstraction too complex | Start minimal, iterate based on usage |
| RISK-02 | YAML config hard to debug | Provide validation errors with line numbers |
| RISK-03 | gevent compatibility issues | Test all skills under gevent early |

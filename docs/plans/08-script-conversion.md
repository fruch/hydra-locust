# Sub-Plan SP8: Script Conversion

> Parent: [high-level-design.md](high-level-design.md) | Phase 3
>
> **Status: NOT STARTED**
>
> **This is a living document.** Update it as development progresses.

## Objective

Build a converter tool (`hydra-locust convert`) that translates Locust Python workload files into Latte Rune scripts, enabling migration between load testing tools.

---

## Requirements & Constraints

| ID | Type | Description |
|----|------|-------------|
| REQ-01 | Requirement | Convert Locust workloads to Latte Rune scripts |
| REQ-02 | Requirement | Handle prepared statements, key distributions, read/write mixes |
| REQ-03 | Requirement | Provide clear warnings for unconvertible constructs |
| REQ-04 | Requirement | Include test suite for round-trip validation |
| CON-01 | Constraint | Python AST complexity limits conversion fidelity |
| CON-02 | Constraint | Some Locust features have no Latte equivalent |

## Design Decisions

| Decision | Choice | Rationale | Alternatives Rejected |
|----------|--------|-----------|----------------------|
| Parsing approach | Python AST module | Standard library, handles all Python syntax | Regex, custom parser |
| Output format | Latte Rune script | Target format for conversion | Generic intermediate |
| CLI integration | `hydra-locust convert` subcommand | Consistent with project CLI | Standalone tool |

## Implementation Tasks

### Phase 8.1: Parser

| # | Task | Description | Validation |
|---|------|-------------|------------|
| 8.1.1 | AST extraction | Extract workload patterns from Locust files | Patterns identified |
| 8.1.2 | Statement extraction | Identify CQL prepared statements | Statements extracted |
| 8.1.3 | Distribution extraction | Identify key distribution patterns | Distributions mapped |

### Phase 8.2: Generator

| # | Task | Description | Validation |
|---|------|-------------|------------|
| 8.2.1 | Rune script template | Template for Latte Rune output | Template valid |
| 8.2.2 | Statement translation | Convert CQL statements to Rune | Output compiles |
| 8.2.3 | Distribution translation | Convert Zipfian/uniform to Rune | Distributions equivalent |
| 8.2.4 | Warning system | Warn on unconvertible patterns | Warnings displayed |

### Phase 8.3: CLI & Testing

| # | Task | Description | Validation |
|---|------|-------------|------------|
| 8.3.1 | CLI subcommand | `hydra-locust convert <input> <output>` | Command works |
| 8.3.2 | Round-trip tests | Convert and validate output | Tests pass |
| 8.3.3 | Example conversions | Convert built-in workloads | Examples work |

---

## Dependencies

| ID | Dependency | Required By |
|----|-----------|-------------|
| DEP-01 | SP1 (Modernize Code) | All tasks |
| DEP-02 | Latte Rune spec | Phase 8.2 |

## Testing Strategy

| ID | Test Type | Description | Validation |
|----|-----------|-------------|------------|
| TEST-01 | Unit | AST extraction | Patterns extracted correctly |
| TEST-02 | Unit | Rune generation | Output is valid Rune |
| TEST-03 | Integration | Full conversion | Converted script runs in Latte |

## Risks

| ID | Risk | Mitigation |
|----|------|-----------|
| RISK-01 | Complex Locust patterns not convertible | Document limitations, warn clearly |
| RISK-02 | Latte Rune API changes | Pin to specific Latte version |

---
name: create-implementation-plan
description: >-
  Create a new implementation plan or sub-plan for hydra-locust features,
  refactoring, or infrastructure work. Use when asked to plan a feature,
  create a design document, write an implementation plan, break down a
  task into phases, or design architecture for a component. Produces
  structured, AI-executable plans with deterministic language.
---

# Create Implementation Plan

Generate implementation plans for the hydra-locust project that are fully executable by AI agents or humans, using deterministic language with zero ambiguity.

## Context

This project follows a phased implementation plan defined in `docs/plans/high-level-design.md` with 11 sub-plans (SP1–SP11). New plans must align with the existing architecture and phasing.

Before writing a plan, read:
1. `docs/plans/high-level-design.md` — master plan and architecture
2. The relevant existing sub-plan(s) for the area being planned

## Plan File Specifications

### Location and Naming

Save in `docs/plans/` directory using the naming convention:

```
docs/plans/[NN]-[component].md
```

Where `NN` is the next available number and `component` describes the area.

### Plan Structure

Every plan must include these sections:

```markdown
# Sub-Plan SPNN: [Title]

> Parent: [high-level-design.md](high-level-design.md) | Phase N
>
> **This is a living document.** Update it as development progresses.

## Objective

[1-2 sentences: what this plan achieves and why it matters]

---

## Requirements & Constraints

| ID | Type | Description |
|----|------|-------------|
| REQ-01 | Requirement | ... |
| CON-01 | Constraint | ... |

## Design Decisions

| Decision | Choice | Rationale | Alternatives Rejected |
|----------|--------|-----------|----------------------|
| ... | ... | ... | ... |

## Implementation Tasks

### Phase N.M: [Phase Title]

| # | Task | Description | Validation |
|---|------|-------------|------------|
| N.M.1 | ... | ... | ... |

## Dependencies

| ID | Dependency | Required By |
|----|-----------|-------------|
| DEP-01 | ... | Task N.M.X |

## Testing Strategy

| ID | Test Type | Description | Validation |
|----|-----------|-------------|------------|
| TEST-01 | Unit | ... | ... |

## Risks

| ID | Risk | Mitigation |
|----|------|-----------|
| RISK-01 | ... | ... |
```

## Writing Standards

### Language

- Use explicit, unambiguous language requiring zero interpretation
- Every task must be independently actionable
- Include specific file paths and code references where known
- Use imperative mood: "Implement X" not "X should be implemented"

### Task Granularity

Each task should be:
- Completable in a single focused session
- Independently testable
- Clear about inputs and expected outputs

### Validation Criteria

Every task must have a validation column that describes how to verify completion. Use concrete criteria:
- "Unit test passes" (not "test it")
- "`uv run pytest tests/test_skills.py` passes"
- "Output matches expected format"

## Living Document Policy

Plans in this project are living documents:
- Update on decision: when an open question is resolved, update immediately
- Prune after research: remove speculative options that were not chosen
- Document reasoning: explain why alternatives were rejected
- Plans serve as source of truth alongside the codebase

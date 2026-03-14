---
name: conventional-commit
description: >-
  Generate standardized commit messages following the Conventional Commits
  specification. Use when asked to commit changes, write a commit message,
  create a conventional commit, or when committing code. Analyzes staged
  changes and produces properly formatted commit messages.
---

# Conventional Commit

Generate commit messages following the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification for the hydra-locust project.

## Workflow

1. Run `git status` to review changed files
2. Run `git diff --cached` to inspect staged changes (or `git diff` for unstaged)
3. Analyze the changes to determine the commit type and scope
4. Construct the commit message following the format below
5. Stage files if needed with `git add <files>`
6. Execute the commit

## Commit Message Format

```
type(scope): description

[optional body]

[optional footer(s)]
```

### Types

| Type | When to Use |
|------|------------|
| `feat` | New feature or capability |
| `fix` | Bug fix |
| `docs` | Documentation only changes |
| `style` | Formatting, whitespace (no code change) |
| `refactor` | Code restructuring (no feature/fix) |
| `perf` | Performance improvement |
| `test` | Adding or updating tests |
| `build` | Build system or dependencies |
| `ci` | CI/CD configuration |
| `chore` | Maintenance tasks |
| `revert` | Reverting a previous commit |

### Scopes for hydra-locust

Use these project-specific scopes:

| Scope | Area |
|-------|------|
| `common` | Shared utilities (common.py) |
| `cql` | CQL/Cassandra workloads |
| `dynamodb` | DynamoDB workloads |
| `prom` | Prometheus metrics |
| `driver` | Driver abstraction layer |
| `skill` | Skill system |
| `bench` | Benchmarks |
| `docker` | Docker configuration |
| `plan` | Design documents and plans |
| `skills` | AI assistant skills |

### Rules

- Description must use imperative mood: "add", not "added" or "adds"
- Description must be lowercase, no period at the end
- Keep the first line under 72 characters
- Body explains **why**, not what (the diff shows what)
- Footer references issues: `Fixes #123`, `Refs #456`
- Breaking changes: add `!` after type/scope and `BREAKING CHANGE:` in footer

### Examples

```
feat(cql): add batch insert workload skill

Implements a batch insert skill for CQL workloads using prepared
statements and configurable batch sizes.

Refs #42
```

```
fix(common): handle empty iterator in iter_shuffle

The shuffle function was raising StopIteration on empty input
instead of returning an empty iterator.
```

```
docs(plan): update phase 1 tasks with implementation decisions
```

```
test(common): add edge case tests for Zipfian distribution
```

```
feat(driver)!: change default connection timeout

BREAKING CHANGE: default connection timeout changed from 5s to 10s
to match scylla-driver defaults.
```

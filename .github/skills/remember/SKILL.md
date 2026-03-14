---
name: remember
description: >-
  Save lessons learned, debugging insights, and project-specific knowledge
  into persistent memory files. Use when asked to remember something,
  save a lesson, record a gotcha, document a pattern, or persist knowledge
  for future sessions. Syntax: /remember [domain] lesson content.
---

# Memory Keeper

Transform debugging sessions, workflow discoveries, and hard-won lessons into persistent, domain-organized knowledge that helps AI assistants find relevant guidance in future sessions.

## Syntax

```
/remember [domain] lesson content
```

- `domain` — Optional. Target a specific domain (e.g., `python`, `cql`, `dynamodb`, `testing`)
- `lesson content` — Required. The lesson to remember

### Examples

```
/remember python gevent monkey-patching must be done before any other imports
/remember cql scylla-driver uses cassandra module namespace, not scylla
/remember dynamodb boto3 requires explicit endpoint_url for Alternator
/remember testing report_timings tests need mock Locust environment
/remember always run uv run ruff check before committing
```

## Memory File Locations

### GitHub Copilot

Memory files are stored as instruction files in `.github/instructions/`:

- **General**: `.github/instructions/memory.instructions.md`
- **Domain-specific**: `.github/instructions/{domain}-memory.instructions.md`

Copilot instruction files use `applyTo` frontmatter for targeted activation:

```yaml
---
description: 'Lessons learned about Python patterns in this project'
applyTo: '**/*.py'
---
```

## Process

1. **Parse input** — Extract domain (if specified) and lesson content
2. **Read existing memory files** — Check what domains already exist
3. **Categorize the learning**:
   - New gotcha / common mistake
   - Enhancement to existing knowledge
   - New best practice or pattern
   - Process improvement
4. **Determine target domain and file paths**
5. **Read the target files** to avoid redundancy
6. **Write the memory** to the instruction files

## Memory File Structure

```markdown
---
description: 'Lessons learned about {domain} in this project'
applyTo: '{relevant glob pattern}'
---

# {Domain} Memory

> Lessons learned and patterns for {domain} in hydra-locust.

## {Lesson Title}

{Concise, actionable lesson content}
```

## Domain Mapping

| Domain | Copilot `applyTo` | Description |
|--------|-------------------|-------------|
| `python` | `**/*.py` | Python language patterns and idioms |
| `cql` | `**/*cql*,**/locustfile*` | CQL protocol and query patterns |
| `dynamodb` | `**/*dynamodb*` | DynamoDB/Alternator specifics |
| `testing` | `**/tests/**,**/*test*` | Testing patterns and gotchas |
| `ci` | `.github/workflows/**` | CI/CD configuration lessons |
| `docker` | `**/Dockerfile*,**/.docker*` | Docker and container patterns |
| `plan` | `docs/plans/**` | Planning and documentation patterns |
| (general) | `**/*` | Cross-cutting lessons |

## Writing Guidelines

- **Generalize from specifics** — Extract reusable patterns
- **Be concrete** — Include code examples when relevant
- **Focus on what TO do** — Positive reinforcement over "don't" instructions
- **Keep it scannable** — Short paragraphs, bullet points, code snippets
- **Explain the why** — Context helps apply the lesson correctly
- **Remove redundancy** — Merge if a lesson duplicates existing knowledge

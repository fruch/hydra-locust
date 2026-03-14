# Sub-Plan SP6: Latte-like Features

> Parent: [high-level-design.md](high-level-design.md) | Phase 3
>
> **Status: NOT STARTED**
>
> **This is a living document.** Update it as development progresses.

## Objective

Implement key features from [latte](https://github.com/scylladb/latte) (Rune-based workload scripts, coordinated-omission awareness, HDR histograms) on top of Locust, while maintaining Locust compatibility for the web UI and distributed mode.

---

## Requirements & Constraints

| ID | Type | Description |
|----|------|-------------|
| REQ-01 | Requirement | Configurable workload profiles (ramp-up, steady-state, ramp-down) |
| REQ-02 | Requirement | Percentile-accurate latency histograms |
| REQ-03 | Requirement | Rate-limiting / throughput-target mode |
| REQ-04 | Requirement | Maintain Locust web UI and distributed mode compatibility |
| CON-01 | Constraint | Must work within Locust's event loop model |
| CON-02 | Constraint | Must not degrade Locust's baseline performance |

## Design Decisions

| Decision | Choice | Rationale | Alternatives Rejected |
|----------|--------|-----------|----------------------|
| Workload profiles | Custom Locust LoadTestShape | Native Locust mechanism for shaping load | External rate controller |
| Histograms | HDR Histogram library | Industry standard, coordinated omission support | numpy histograms |
| Rate limiting | Token bucket algorithm | Simple, proven, predictable | Leaky bucket, PID controller |

## Implementation Tasks

### Phase 6.1: Workload Profiles

| # | Task | Description | Validation |
|---|------|-------------|------------|
| 6.1.1 | Ramp-up profile | Gradually increase users over time | User count ramps correctly |
| 6.1.2 | Steady-state profile | Maintain constant user count | User count stable |
| 6.1.3 | Ramp-down profile | Gradually decrease users | User count decreases |
| 6.1.4 | Composite profiles | Chain ramp-up → steady → ramp-down | Full profile executes |

### Phase 6.2: Latency Measurement

| # | Task | Description | Validation |
|---|------|-------------|------------|
| 6.2.1 | HDR histogram integration | Record latencies in HDR histograms | Histograms populated |
| 6.2.2 | Percentile reporting | Report p50, p95, p99, p99.9, max | Percentiles accurate |
| 6.2.3 | Coordinated omission detection | Detect and report CO artifacts | CO detected in synthetic test |

### Phase 6.3: Rate Limiting

| # | Task | Description | Validation |
|---|------|-------------|------------|
| 6.3.1 | Token bucket rate limiter | Implement rate limiting for throughput targets | Rate within 5% of target |
| 6.3.2 | Rate limit configuration | CLI flag and config for target throughput | Config accepted |
| 6.3.3 | Rate limit reporting | Report actual vs. target throughput | Reports match |

---

## Dependencies

| ID | Dependency | Required By |
|----|-----------|-------------|
| DEP-01 | SP1 (Modernize Code) | All tasks |
| DEP-02 | SP9 (HDR Histograms) | Phase 6.2 |

## Testing Strategy

| ID | Test Type | Description | Validation |
|----|-----------|-------------|------------|
| TEST-01 | Unit | LoadTestShape profiles | Shape produces expected user counts |
| TEST-02 | Unit | Rate limiter accuracy | Rate within tolerance |
| TEST-03 | Integration | Full profile run | Profile executes against container |

## Risks

| ID | Risk | Mitigation |
|----|------|-----------|
| RISK-01 | Locust LoadTestShape limitations | Prototype early, fallback to custom scheduler |
| RISK-02 | HDR histogram Python library performance | Benchmark library, consider C extension |

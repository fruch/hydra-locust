# Sub-Plan SP10: Prometheus Support

> Parent: [high-level-design.md](high-level-design.md) | Phase 4
>
> **Status: IN PROGRESS** — Basic collector implemented in `prom_collector.py` (2026-03-14)
>
> **This is a living document.** Update it as development progresses.

## Objective

Extend the existing Prometheus metrics exporter into a full-featured monitoring solution with per-operation histograms, Grafana dashboards, and push-gateway support for short-lived tests.

---

## Requirements & Constraints

| ID | Type | Description |
|----|------|-------------|
| REQ-01 | Requirement | Per-operation latency histograms |
| REQ-02 | Requirement | Throughput counters and error rates |
| REQ-03 | Requirement | Sample Grafana dashboard JSON |
| REQ-04 | Requirement | Push-gateway mode for short-lived test runs |
| CON-01 | Constraint | Must not impact Locust performance significantly |
| CON-02 | Constraint | Must work in distributed Locust mode |

## Design Decisions

| Decision | Choice | Rationale | Alternatives Rejected |
|----------|--------|-----------|----------------------|
| Metrics library | `prometheus-client` | Standard Python Prometheus client | StatsD, custom |
| Histogram buckets | Default + extended high-latency | Cover typical database latency range | Linear buckets |
| Dashboard | Grafana JSON provisioning | Industry standard, version-controlled | Prometheus console templates |

## Implementation Tasks

### Phase 10.1: Enhanced Metrics

| # | Task | Description | Validation | Status |
|---|------|-------------|------------|--------|
| 10.1.1 | Basic collector | Collect stats from Locust runner | Metrics exposed on :9000 | ✅ Done |
| 10.1.2 | Per-operation histograms | Histogram per request type | Histograms in /metrics | ☐ TODO |
| 10.1.3 | Error rate counters | Count errors per request type | Counters in /metrics | ☐ TODO |
| 10.1.4 | Connection pool metrics | Track driver connection pool stats | Metrics in /metrics | ☐ TODO |

### Phase 10.2: Grafana Dashboard

| # | Task | Description | Validation |
|---|------|-------------|------------|
| 10.2.1 | Dashboard JSON | Create Grafana dashboard for hydra-locust | Dashboard imports correctly |
| 10.2.2 | Dashboard documentation | How to import and use the dashboard | Guide works |

### Phase 10.3: Push Gateway

| # | Task | Description | Validation |
|---|------|-------------|------------|
| 10.3.1 | Push gateway integration | Push metrics to Prometheus push gateway | Metrics visible in Prometheus |
| 10.3.2 | Push gateway config | CLI flag and config for push gateway URL | Config accepted |
| 10.3.3 | Final push on exit | Push final metrics when test completes | Final metrics captured |

---

## Dependencies

| ID | Dependency | Required By |
|----|-----------|-------------|
| DEP-01 | SP1 (Modernize Code) | All tasks |
| DEP-02 | `prometheus-client` package | Already installed |

## Testing Strategy

| ID | Test Type | Description | Validation |
|----|-----------|-------------|------------|
| TEST-01 | Unit | Metric collection and formatting | Metrics correct |
| TEST-02 | Integration | Prometheus scraping metrics endpoint | Scrape succeeds |
| TEST-03 | Integration | Push gateway push | Metrics visible |

## Risks

| ID | Risk | Mitigation |
|----|------|-----------|
| RISK-01 | Metrics overhead under high load | Benchmark collector overhead |
| RISK-02 | Distributed mode metric aggregation | Only collect on master node |

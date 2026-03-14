# Sub-Plan SP9: HDR Histograms & Coordinated Omission

> Parent: [high-level-design.md](high-level-design.md) | Phase 4
>
> **Status: NOT STARTED**
>
> **This is a living document.** Update it as development progresses.

## Objective

Integrate HDR Histogram support for percentile-accurate latency recording, implement coordinated-omission detection and correction, and support multiple output formats (HDR log, JSON, CSV).

---

## Requirements & Constraints

| ID | Type | Description |
|----|------|-------------|
| REQ-01 | Requirement | Integrate HDR Histogram library for latency recording |
| REQ-02 | Requirement | Output in HDR Histogram log format |
| REQ-03 | Requirement | Compatible with HistogramLogAnalyzer |
| REQ-04 | Requirement | Implement coordinated-omission detection and correction |
| REQ-05 | Requirement | Support HDR log, JSON, and CSV output formats |
| CON-01 | Constraint | Must not significantly impact measurement overhead |
| CON-02 | Constraint | Must integrate with Locust's event system |

## Design Decisions

| Decision | Choice | Rationale | Alternatives Rejected |
|----------|--------|-----------|----------------------|
| HDR library | `hdrhistogram` PyPI package | Python port of HdrHistogram, well-maintained | numpy-based histograms |
| CO correction | Gil Tene's method | Industry standard approach | Custom correction |
| Output format | HDR log format | Compatible with standard analysis tools | Custom binary format |

## Implementation Tasks

### Phase 9.1: HDR Integration

| # | Task | Description | Validation |
|---|------|-------------|------------|
| 9.1.1 | Add `hdrhistogram` dependency | Add to pyproject.toml | `uv sync` succeeds |
| 9.1.2 | Histogram collector | Record latencies per request type | Histograms populated |
| 9.1.3 | Locust event integration | Hook into Locust success/failure events | Events recorded |

### Phase 9.2: Coordinated Omission

| # | Task | Description | Validation |
|---|------|-------------|------------|
| 9.2.1 | CO detection | Detect gaps in expected request schedule | Gaps detected in synthetic test |
| 9.2.2 | CO correction | Apply correction to latency values | Corrected percentiles realistic |
| 9.2.3 | CO reporting | Report corrected vs. uncorrected percentiles | Both values in output |

### Phase 9.3: Output Formats

| # | Task | Description | Validation |
|---|------|-------------|------------|
| 9.3.1 | HDR log output | Write HDR Histogram log format | HistogramLogAnalyzer reads file |
| 9.3.2 | JSON output | Export percentiles as JSON | JSON is valid |
| 9.3.3 | CSV output | Export percentiles as CSV | CSV is valid |
| 9.3.4 | CLI flags for output | `--hdr-output`, `--json-output`, `--csv-output` | Flags accepted |

---

## Dependencies

| ID | Dependency | Required By |
|----|-----------|-------------|
| DEP-01 | SP1 (Modernize Code) | All tasks |
| DEP-02 | `hdrhistogram` package | Phase 9.1 |

## Testing Strategy

| ID | Test Type | Description | Validation |
|----|-----------|-------------|------------|
| TEST-01 | Unit | Histogram recording and percentile calculation | Values accurate |
| TEST-02 | Unit | CO detection with synthetic gaps | Gaps found |
| TEST-03 | Unit | Output format validation | Files parse correctly |
| TEST-04 | Integration | Full workload with HDR output | Output file readable |

## Risks

| ID | Risk | Mitigation |
|----|------|-----------|
| RISK-01 | `hdrhistogram` Python package performance | Benchmark overhead, consider C extension |
| RISK-02 | CO correction accuracy | Validate against known-good reference implementations |

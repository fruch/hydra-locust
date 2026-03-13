# Hydra-Locust Roadmap

## 1. Modernize the Code

### 1.1 UV and pyproject.toml

- Migrate from `requirements.in` / `requirements.txt` to a `pyproject.toml`-based project layout
- Adopt [uv](https://github.com/astral-sh/uv) as the package manager and virtual-environment tool
- Add a `uv.lock` lock file for reproducible installs
- Remove legacy `requirements*.in` / `requirements*.txt` files once migration is complete

### 1.2 Update Dependencies (especially the driver)

- Upgrade `scylla-driver` to the latest release
- Upgrade `locust`, `boto3`, `aioboto3`, `numpy`, `prometheus-client`, and all transitive dependencies
- Pin minimum supported Python version in `pyproject.toml`
- Set up Dependabot or Renovate for automated dependency updates

### 1.3 Update Documentation

- Rewrite `README.md` to reflect the new build / install workflow (uv, pyproject.toml)
- Add a `docs/` site (e.g. MkDocs or Sphinx) with:
  - Getting-started guide
  - Configuration reference
  - Architecture overview
  - Contributing guide

---

## 2. Introduce Skill System

Collect and adapt community-built Python skills, using the [coodie](https://github.com/scylladb/coodie) project's skill architecture as a reference model.

- Survey existing community Python skills and workload patterns (coodie, open-source Locust plugins, etc.) and adapt the best ones for hydra-locust
- Design a **skill** abstraction that encapsulates a reusable workload pattern (e.g. read-heavy, write-heavy, mixed, scan, batch)
- Allow users to compose skills declaratively (YAML / TOML config or Python API)
- Ship a library of built-in skills for common Cassandra / DynamoDB workloads, seeded from community examples
- Support user-defined custom skills loaded from external modules

---

## 3. Introduce Tests, Integration Tests, and Benchmarks

Follow the [coodie](https://github.com/scylladb/coodie) project's testing approach as a reference — it demonstrates well-structured unit tests, integration tests, and benchmarks for a driver/load-testing tool.

### 3.1 Unit Tests

- Add a `tests/` directory with pytest-based unit tests for `common.py` utilities (shuffling, Zipfian distribution, timing decorators, etc.)
- Integrate test runs into CI (GitHub Actions)

### 3.2 Integration Tests

- Stand up a ScyllaDB / Cassandra container in CI and run end-to-end Locust scenarios against it (similar to coodie's integration test setup)
- Stand up a DynamoDB-compatible container (e.g. ScyllaDB Alternator or DynamoDB Local) for DynamoDB integration tests

### 3.3 Benchmarks

- Create reproducible micro-benchmarks for the driver layer and data-generation helpers, modeled on coodie's benchmark suite
- Track benchmark results over time to detect performance regressions

---

## 4. Support Pluggable Drivers

- Refactor the driver layer behind a common **Driver** interface / protocol so that the Cassandra/Scylla driver is no longer hard-wired
- Define a minimal driver contract (connect, prepare, execute, close) that any backend must implement
- Allow selecting the driver via configuration or command-line flag (e.g. `--driver scylla` / `--driver coodie`)
- Document how third-party drivers can be plugged in by implementing the interface

---

## 5. Support Coodie Usage

Building on the pluggable-driver interface from Section 4:

- Implement a [coodie](https://github.com/scylladb/coodie) (Rust-based) driver adapter
- Provide example workloads that exercise coodie-specific features (e.g. shard-aware routing)
- Benchmark coodie vs. scylla-driver under identical workloads and publish results
- Document setup, installation, and usage of coodie within hydra-locust

---

## 6. Support Latte-like Features Based on Locust

- Identify key features of [latte](https://github.com/scylladb/latte) (Rune-based workload scripts, coordinated-omission awareness, HDR histograms, etc.)
- Implement equivalent capabilities on top of Locust:
  - Configurable workload profiles (ramp-up, steady-state, ramp-down)
  - Percentile-accurate latency histograms
  - Rate-limiting / throughput-target mode
- Maintain Locust compatibility so users can still leverage the Locust web UI and distributed mode

---

## 7. Review Locust Performance vs. Other Python Tools — Support Multiple Options

- Benchmark Locust against alternative Python load-generation frameworks (e.g. [Molotov](https://github.com/tarekziade/molotov), [Grizzly](https://github.com/Biometria-se/grizzly), raw asyncio loops)
- Publish comparison results (throughput, latency overhead, resource usage)
- If alternatives prove significantly better for certain workloads, support them as selectable backends behind the same hydra-locust interface

---

## 8. Conversion from Locust Scripts to Latte Rune Scripts

- Build a **converter** tool (`hydra-locust convert`) that translates Locust Python workload files into Latte Rune scripts
- Handle common patterns: prepared statements, key distributions, read/write mixes
- Provide clear warnings for constructs that cannot be automatically translated
- Include a test suite that round-trips representative workloads

---

## 9. HDR Output Support and Coordinated Omission Support

- Integrate an HDR Histogram library (e.g. [hdrhistogram](https://pypi.org/project/hdrhistogram/)) for latency recording
- Output results in HDR Histogram log format compatible with [HistogramLogAnalyzer](https://github.com/HdrHistogram/HistogramLogAnalyzer)
- Implement coordinated-omission detection and correction so that reported latencies reflect real user-perceived delays
- Allow exporting results in multiple formats (HDR log, JSON, CSV)

---

## 10. Prometheus Support

- Extend the existing `prom_collector.py` into a full-featured Prometheus exporter
- Expose per-operation latency histograms, throughput counters, and error rates
- Provide a sample Grafana dashboard JSON for out-of-the-box monitoring
- Support push-gateway mode for short-lived test runs

---

## 11. Frontend for Other Stress Tools with Common Command-Line Interface

Provide a **unified CLI frontend** that can drive any of the following backends through a single, consistent command-line interface:

| Backend              | Description                          |
| -------------------- | ------------------------------------ |
| **latte**            | Rune-based Cassandra stress tool     |
| **cassandra-stress** | Built-in Cassandra stress utility    |
| **scylla-bench**     | Go-based Scylla benchmark tool       |
| **YCSB**             | Yahoo! Cloud Serving Benchmark       |

### Goals

- Common flags for connection parameters, duration, concurrency, and result output
- Translate the common CLI into each tool's native arguments
- Aggregate and normalize results from all backends into a single report format
- Support running multiple backends in parallel for comparative benchmarking

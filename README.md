# hydra-locust

Locust-based CQL/DynamoDB load testing tool for ScyllaDB and Cassandra.

## Requirements

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

## Install

```bash
# Using uv (recommended)
uv sync

# Or using pip
python3 -m venv .venv
source .venv/bin/activate
pip install .
```

## Run

```bash
docker run -d -p 8080:8080 -p 9042:9042 scylladb/scylla --alternator-port 8080 --alternator-write-isolation=always

# run dynamodb example
uv run locust -f dynamodb_case1.py --host http://127.0.0.1:8080 --headless --users 30 -t 1m  -r 30


# run cql example
uv run locust -f locustfile.py --host 172.17.0.2 --headless --users 30 -t 1m -r 30
```

## Development

```bash
# install with dev dependencies
uv sync --dev

# run tests
uv run pytest

# run linter
uv run ruff check .
```

## Profiling

```bash
sudo apt-get install libgtk-3-dev
pip install runsnakerun
python -m cProfile -o benchmark.prof benchmark.py

runsnake benchmark.prof
```

## Building Docker Image

```bash
export HYDRA_LOCUST_IMAGE=scylladb/hydra-loaders:locust-py3-$(date +'%Y%m%d')
docker build . -t ${HYDRA_LOCUST_IMAGE}
docker push ${HYDRA_LOCUST_IMAGE}
echo "${HYDRA_LOCUST_IMAGE}" > image
```

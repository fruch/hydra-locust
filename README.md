# hydra-locust

## install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## run

```bash
docker run -d -p 8080:8080 -p 9042:9042 scylladb/scylla --alternator-port 8080 --alternator-write-isolation=always

# run dynamodb example
locust -f dynamodb_case1.py --host http://127.0.0.1:8080 --headless --users 30 -t 1m  -r 30


# run cql example
locust -f locustfile.py --host 172.17.0.2 --headless --users 30 -t 1m -r 30
```

## profiling

```bash
sudo apt-get install libgtk-3-dev
pip install runsnakerun
python -m cProfile -o benchmark.prof benchmark.py

runshake benchmark.prof
```

## building docker image

```bash
export HYDRA_LOCUST_IMAGE=scylladb/hydra-loaders:locust-py3-$(date +'%Y%m%d')
docker build . -t ${HYDRA_LOCUST_IMAGE}
docker push ${HYDRA_LOCUST_IMAGE}
echo "${HYDRA_LOCUST_IMAGE}" > image
```

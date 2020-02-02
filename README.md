# hydra-locust


## install

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## run
```
docker run -d -p 8080:8080 -p 9042:9042 scylladb/scylla:3.2.0 --alternator-port 8080

# run dynamodb example
locust -f dynamodb_case1.py --host http://127.0.0.1:8080 --no-web -c 30 -t 5m  -r 30

# run cql example
locust -f locustfile.py --host 127.0.0.1 --no-web -c 30 -t 5m  -r 30
```

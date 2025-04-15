Gliner deployement with Ray serve with GRPC serving

Commands for deployement
Deployement can be done in 2 ways
1. Python API

```sh
python gliner_server.py
python grpc_server.py
```

2. Serve Config yaml

```sh
serve run config.yaml
```

Clients
-------

There are 3 clients to run sample inference, utilze the same

```sh
python grpc_client.py
python grpc_client2.py
python grpc_client3.py
```


Load test Experiments
-----------------
TLDR :- ghz is chosen as a load test tool for simplicity

Total experiment for load tests has been tried with 3 types

1. locust

```sh
locust -f locustfile.py --headless -u 10  --run-time 2m
```

2. gzh


CLI interface calling for benchmarking
```sh
ghz --insecure \
    --proto gliner_protos.proto \
    --call Gliner.infer \
    --data-file payload.json \
    --concurrency 10 \
    --total 10 \
    localhost:9000
```

Script based benchmarking with various load test configuration

```sh
source gliner_load_benchmarks.sh
```

3. threadpool

configurations are updated internally
```sh
python load_test.py
```


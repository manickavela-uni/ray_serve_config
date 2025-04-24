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
chmod +x run_grpc_benchmark.sh

# Run a specific test:
./run_grpc_benchmark.sh load
./run_grpc_benchmark.sh soak
./run_grpc_benchmark.sh spike
./run_grpc_benchmark.sh stress
```

3. threadpool

configurations are updated internally
```sh
python load_test.py
```

curl 
```sh
curl -X POST http://localhost:8000/unifit_inference_worker/ \
     -H "Content-Type: application/json" \
     -d '{"speaker": "agent", "text": "hello good afternoon welcome to my name is how can i help you"}'
```


curl -X POST http://localhost:8000/ \
     -H "serve_multiplexed_model_id:f7a88bc2-49eb-4330-96eb-9ea5488fd2b2" \
     -H "Content-Type: application/json" \
     -d '{"speaker": "agent", "text": "hello good afternoon welcome to my name is how can i help you"}'

     f7a88bc2-49eb-4330-96eb-9ea5488fd2b2
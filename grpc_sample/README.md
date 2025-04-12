grpc_sample is a sample mentioned as part of Ray Serve 
https://docs.ray.io/en/latest/serve/advanced-guides/grpc-guide.html

Commands for deployement
Deployement can be done in 2 ways
1. Python API

```sh
python start_server.py
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
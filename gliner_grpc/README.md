Gliner deployement with Ray serve with GRPC serving

Commands for deployement
There are 3 ways to start the deployement
1. CLI

```sh
ray start --head
serve start \
  --grpc-port 9000 \
  --grpc-servicer-functions gliner_protos_pb2_grpc.add_GlinerServicer_to_server
```

2. Python API

```sh
python gliner_server.py
python grpc_server.py
```

3. Serve Config yaml

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
from ray import serve
from ray.serve.config import gRPCOptions


grpc_port = 9000
grpc_servicer_functions = [
    "gliner_protos_pb2_grpc.infer",
]
serve.start(
    grpc_options=gRPCOptions(
        port=grpc_port,
        grpc_servicer_functions=grpc_servicer_functions,
    ),
)
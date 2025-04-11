from ray import serve
from ray.serve.config import gRPCOptions


grpc_port = 9000
grpc_servicer_functions = [
    "user_defined_protos_pb2_grpc.add_UserDefinedServiceServicer_to_server",
    "user_defined_protos_pb2_grpc.add_ImageClassificationServiceServicer_to_server",
]
serve.start(
    grpc_options=gRPCOptions(
        port=grpc_port,
        grpc_servicer_functions=grpc_servicer_functions,
    ),
)

'''
    This is a sample gRPC client that sends a request to a gRPC server using multiplexing.
    Streaming methos is demonstrated
'''
import grpc
from user_defined_protos_pb2_grpc import UserDefinedServiceStub
from user_defined_protos_pb2 import UserDefinedMessage


channel = grpc.insecure_channel("localhost:9000")
stub = UserDefinedServiceStub(channel)
request = UserDefinedMessage(name="foo", num=30, origin="bar")
metadata = (("application", "app1"),)

responses = stub.Streaming(request=request, metadata=metadata)
for response in responses:
    print(f"greeting: {response.greeting}")  # greeting: n: Hello foo from bar
    print(f"num: {response.num}")  # num: 60 + n
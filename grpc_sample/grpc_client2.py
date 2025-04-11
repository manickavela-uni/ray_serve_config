'''
    Sample with meta data passed to the server
'''

import grpc
from user_defined_protos_pb2_grpc import UserDefinedServiceStub
from user_defined_protos_pb2 import UserDefinedMessage2


channel = grpc.insecure_channel("localhost:9000")
stub = UserDefinedServiceStub(channel)
request = UserDefinedMessage2()
app_name = "app1"
request_id = "123"
multiplexed_model_id = "999"
metadata = (
    ("application", app_name),
    ("request_id", request_id),
    ("multiplexed_model_id", multiplexed_model_id),
)

response, call = stub.Multiplexing.with_call(request=request, metadata=metadata)
print(f"greeting: {response.greeting}")  # "Method2 called model, loading model: 999"
for key, value in call.trailing_metadata():
    print(f"trailing metadata key: {key}, value {value}")  # "request_id: 123"
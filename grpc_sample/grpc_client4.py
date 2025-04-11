import grpc
from user_defined_protos_pb2_grpc import ImageClassificationServiceStub
from user_defined_protos_pb2 import ImageData


channel = grpc.insecure_channel("localhost:9000")
stub = ImageClassificationServiceStub(channel)
request = ImageData(url="https://github.com/pytorch/hub/raw/master/images/dog.jpg")
metadata = (("application", "app2"),)  # Make sure application metadata is passed.

response, call = stub.Predict.with_call(request=request, metadata=metadata)
print(f"status code: {call.code()}")  # grpc.StatusCode.OK
print(f"Classes: {response.classes}")  # ['Samoyed', ...]
print(f"Probabilities: {response.probabilities}")  # [0.8846230506896973, ...]
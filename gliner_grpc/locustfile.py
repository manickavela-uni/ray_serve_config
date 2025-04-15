from locust import User, task, between, events
import grpc
import time
import random
from gliner_protos_pb2 import TextsLabels
import gliner_protos_pb2_grpc
from locust import constant
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=50)

class GrpcGlinerClient:
    def __init__(self, host: str = "localhost:9000"):
        self.channel = grpc.insecure_channel(host)
        self.stub = gliner_protos_pb2_grpc.GlinerStub(self.channel)

    def infer(self, texts, labels, threshold=0.1):
        request = TextsLabels(texts=texts, labels=labels, threshold=threshold)
        return self.stub.infer(request)

class GlinerUser(User):
    wait_time = constant(0)

    def on_start(self):
        self.channel = grpc.insecure_channel("localhost:9000")
        self.stub = gliner_protos_pb2_grpc.GlinerStub(self.channel)

        self.texts = [
            "agent: hi thanks for calling voya, customer: hi, agent: this is john how can i help you, customer: hi john this is maria..."
        ]
        self.labels = ["agent name", "customer name", "zip code"]
        self.threshold = 0.1

    @task
    def infer_text(self):
        start_time = time.time()

        try:
            future = executor.submit(
                self.stub.infer,
                TextsLabels(texts=self.texts, labels=self.labels, threshold=self.threshold)
            )
            response = future.result(timeout=5)

            total_time = int((time.time() - start_time) * 1000)

            events.request.fire(
                request_type="gRPC",
                name="infer",
                response_time=total_time,
                response_length=len(response.SerializeToString())  # Optional
            )

        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)

            events.request.fire(
                request_type="gRPC",
                name="infer",
                response_time=total_time,
                exception=e
            )
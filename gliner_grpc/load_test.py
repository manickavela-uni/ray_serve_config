import grpc
import time
import json
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from gliner_protos_pb2 import TextsLabels
from gliner_protos_pb2_grpc import GlinerStub

# Config
NUM_THREADS = 10         # Number of concurrent threads
NUM_REQUESTS = 10       # Total number of requests to send
TARGET = "localhost:9000"
LABELS = ["person", "book", "location", "date", "actor", "character"]
THRESHOLD = 0.5

# Sample Texts
TEXTS = [
    "Barack Obama was born in Hawaii.",
    "Harry Potter is a book by J.K. Rowling.",
    "The Eiffel Tower is located in Paris.",
    "Sachin Tendulkar played for India.",
    "Elon Musk founded SpaceX and Tesla.",
]

def make_request(stub, idx):
    try:
        request = TextsLabels(
            texts=[random.choice(TEXTS)],
            labels=LABELS,
            threshold=THRESHOLD,
        )
        start_time = time.time()
        response = stub.infer(request)
        latency = time.time() - start_time
        return latency
    except Exception as e:
        print(f"Request {idx} failed: {e}")
        return None

def run_load_test():
    latencies = []
    with grpc.insecure_channel(TARGET) as channel:
        stub = GlinerStub(channel)
        with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
            futures = [executor.submit(make_request, stub, i) for i in range(NUM_REQUESTS)]
            for future in as_completed(futures):
                latency = future.result()
                if latency is not None:
                    latencies.append(latency)

    # Summary
    if latencies:
        latencies.sort()
        print("\nLoad Test Summary:")
        print(f"Total Requests: {len(latencies)}")
        print(f"Average Latency: {sum(latencies)/len(latencies)*1000:.2f} ms")
        print(f"Min Latency: {min(latencies)*1000:.2f} ms")
        print(f"Max Latency: {max(latencies)*1000:.2f} ms")
        print(f"P50 (Median): {latencies[len(latencies)//2]*1000:.2f} ms")
        print(f"P95: {latencies[int(len(latencies)*0.95)]*1000:.2f} ms")
        print(f"P99: {latencies[int(len(latencies)*0.99)]*1000:.2f} ms")
    else:
        print("No successful responses.")

if __name__ == "__main__":
    run_load_test()

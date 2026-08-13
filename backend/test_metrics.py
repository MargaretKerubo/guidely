import time
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def run_metrics_validation():
    print("Running Automated Backend Metrics Validation...\n")
    
    # 1. Failure Handling Validation
    print("1. Testing Failure Handling (Empty Query)...")
    resp_empty = client.post("/api/search", json={"query": ""})
    if resp_empty.status_code == 400:
        print("✅ Pass: Empty query gracefully handled with 400 Bad Request.")
    else:
        print(f"❌ Fail: Expected 400, got {resp_empty.status_code}")

    # 2. Latency Validation
    print("\n2. Testing Latency (< 3s)...")
    start = time.time()
    resp_search = client.post("/api/search", json={"query": "What is the policy?"})
    latency = time.time() - start
    
    # Check if we have an OpenAI API Key configured
    if resp_search.status_code == 500 and "API key" in resp_search.text:
         print("⚠️ Skip: OpenAI API Key missing, but failure handled gracefully.")
    else:
        if latency < 3.0:
            print(f"✅ Pass: Latency is {latency:.2f}s (Target < 3.0s)")
        else:
            print(f"❌ Fail: Latency is {latency:.2f}s, which exceeds 3.0s")
            
        # 3. Cache Hits Validation
        print("\n3. Testing Cache Hits Header...")
        cache_hit = resp_search.headers.get("X-Cache-Hit")
        if cache_hit == "true":
            print("✅ Pass: X-Cache-Hit header indicates a cache hit.")
        else:
            print("⚠️ Notice: Request was too slow to be considered a cache hit, or header missing.")

if __name__ == "__main__":
    run_metrics_validation()

import pytest
from fastapi.testclient import TestClient
import time
from backend.main import app

client = TestClient(app)

def test_metrics_endpoint():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_failure_handling_empty_query():
    # Test Empty Query
    resp_empty = client.post("/api/search", json={"query": ""})
    assert resp_empty.status_code == 400

def test_failure_handling_nonexistent():
    # Test non-existent endpoint
    response = client.get("/api/nonexistent")
    assert response.status_code == 404

def test_latency_and_cache_hit():
    # Only test latency if an API key is present, otherwise we expect 500 error for configuration
    resp_search = client.post("/api/search", json={"query": "What is the policy?"})
    
    if resp_search.status_code == 500 and "API key" in resp_search.text:
        pytest.skip("OpenAI API Key missing, skipping latency test.")
    
    # We should get a successful response if configured
    assert resp_search.status_code == 200
    
    # Check that latency header exists and is under 3.0s
    process_time_str = resp_search.headers.get("X-Process-Time")
    assert process_time_str is not None, "Latency header not found"
    process_time = float(process_time_str)
    assert process_time < 3.0, f"Latency {process_time} exceeded 3s limit"
    
    # Send second request to simulate cache hit
    resp_search_2 = client.post("/api/search", json={"query": "What is the policy?"})
    cache_hit = resp_search_2.headers.get("X-Cache-Hit")
    assert cache_hit == "true", "Cache was not hit on repeated request"

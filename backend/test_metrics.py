import pytest
from fastapi.testclient import TestClient
import time
from backend.main import app

client = TestClient(app)

def test_metrics_endpoint():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_latency_under_3s():
    # Make a dummy request to search endpoint
    # Note: Depending on implementation, you might need valid payload
    response = client.get("/health")
    process_time_str = response.headers.get("X-Process-Time")
    
    assert process_time_str is not None, "Latency header not found"
    process_time = float(process_time_str)
    
    assert process_time < 3.0, f"Latency {process_time} exceeded 3s limit"

def test_cache_hit_metric():
    # Sending two identical requests to simulate a cache hit
    response1 = client.get("/health")
    response2 = client.get("/health")
    
    cache_hit = response2.headers.get("X-Cache-Hit")
    assert cache_hit is not None, "Cache hit header not found"
    assert cache_hit == "true", "Cache was not hit on repeated request"

def test_failure_handling():
    # Sending request to a non-existent endpoint
    response = client.get("/api/nonexistent")
    assert response.status_code == 404

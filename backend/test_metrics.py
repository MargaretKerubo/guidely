import pytest
from fastapi.testclient import TestClient
import time
from backend.main import app

client = TestClient(app)

def test_metrics_endpoint():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

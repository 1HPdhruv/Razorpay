import pytest
from fastapi.testclient import TestClient
from app.main import app
import os
import json
from app.core.config import settings

client = TestClient(app)

def test_get_transactions_not_empty():
    # Only test if dataset generated
    if (settings.DATA_DIR / "train" / "transactions.csv").exists():
        response = client.get("/api/transactions")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

def test_get_patterns_not_empty():
    if (settings.DATA_DIR / "discovered_patterns.json").exists():
        response = client.get("/api/patterns")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

def test_get_pattern_by_id():
    patterns_path = settings.DATA_DIR / "discovered_patterns.json"
    if patterns_path.exists():
        with open(patterns_path, "r") as f:
            patterns = json.load(f)
        if len(patterns) > 0:
            first_id = patterns[0]["pattern_id"]
            response = client.get(f"/api/patterns/{first_id}")
            assert response.status_code == 200
            data = response.json()
            assert data["pattern_id"] == first_id

def test_health_metrics():
    if (settings.DATA_DIR / "manifest.json").exists():
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert "transaction_count" in data
        assert data["transaction_count"] > 0
        
        if (settings.DATA_DIR / "discovered_patterns.json").exists():
            assert "pattern_count" in data
            assert data["pattern_count"] > 0

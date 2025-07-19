"""
Health check tests for SprintLens API.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "version" in data
    assert "services" in data

def test_readiness_check():
    """Test readiness check endpoint."""
    response = client.get("/health/ready")
    assert response.status_code in [200, 503]  # 503 if services not configured

def test_liveness_check():
    """Test liveness check endpoint."""
    response = client.get("/health/live")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "alive"

def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data

def test_api_info_endpoint():
    """Test API info endpoint."""
    response = client.get("/api")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "SprintLens API"
    assert "integrations" in data
    assert "endpoints" in data 
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
import sys

# Mock redis BEFORE importing main.
# Why? main.py tries to connect to Redis the moment it's imported.
# There's no Redis in the pipeline, so we fake it to avoid a crash.
sys.modules['redis'] = MagicMock()

from main import app

client = TestClient(app)


def test_create_job():
    """Test that submitting a job returns a job_id"""
    with patch('main.r') as mock_redis:
        mock_redis.lpush = MagicMock()
        mock_redis.hset = MagicMock()
        response = client.post("/jobs")
        assert response.status_code == 200
        assert "job_id" in response.json()


def test_get_job_found():
    """Test that we can retrieve a completed job status"""
    with patch('main.r') as mock_redis:
        mock_redis.hget = MagicMock(return_value=b"completed")
        response = client.get("/jobs/some-fake-id")
        assert response.status_code == 200
        assert response.json()["status"] == "completed"


def test_get_job_not_found():
    """Test that a missing job returns an error"""
    with patch('main.r') as mock_redis:
        mock_redis.hget = MagicMock(return_value=None)
        response = client.get("/jobs/nonexistent-id")
        assert response.status_code == 200
        assert "error" in response.json()


def test_health_endpoint():
    """Test that the health endpoint returns ok"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
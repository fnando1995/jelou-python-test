import sqlite3
import pytest
from fastapi.testclient import TestClient
import sys
import os
import io
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..","app")))
from app.main import app
import pandas as pd
from app.routers.auth import create_access_token
from datetime import timedelta

client = TestClient(app)

@pytest.fixture
def sample_csv():
    """Mock a valid CSV file for testing, using provided dataset."""
    csv_data = open("tests/sample.csv").read()
    return io.BytesIO(csv_data.encode("utf-8"))

@pytest.fixture
def ingest_data(sample_csv):
    """Upload CSV data before testing insights."""
    files = {"file": ("sample.csv", sample_csv, "text/csv")}
    response = client.post("/ingest/", files=files)
    assert response.status_code == 200

@pytest.fixture
def auth_token():
    """Create a test user and obtain a JWT token."""
    
    register_response = client.post("/auth/", json={"username": "test_user", "password": "test123"})
    assert register_response.status_code == 201  
    login_response = client.post("/auth/token", data={"username": "test_user", "password": "test123"})
    assert login_response.status_code == 200
    return login_response.json()["access_token"]

def test_unauthorized_access():
    """Ensure unauthorized requests are rejected."""
    
    response = client.get("/companies/AppleSupport/ai-insights")
    assert response.status_code == 401  

    
def test_get_valid_insights(ingest_data, auth_token):
    """Test insights retrieval for a valid company_id (author_id exists)."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get("/companies/AppleSupport/ai-insights", headers=headers)

    assert response.status_code == 200
    data = response.json()
    data = data["insights"]
    assert len(data)>0
    assert "issue" in data[0]
    assert "percentage" in data[0]
    assert "sentiment" in data[0]


def test_get_insights_invalid_company(auth_token):
    """Test insights retrieval for an invalid company_id (author_id not in dataset)."""
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get("/companies/nonexistent_id/ai-insights", headers=headers)

    assert response.status_code == 200
    data = response.json()
    data = data["insights"]
    assert len(data) == 0

import pytest
from fastapi.testclient import TestClient
import sys
import os
import io
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..","app")))
from app.main import app

client = TestClient(app)

@pytest.fixture
def sample_csv():
    """Mock a valid CSV file for testing, using provided dataset."""
    csv_data = open("tests/sample.csv").read()
    return io.BytesIO(csv_data.encode("utf-8"))

def test_ingest_valid_csv(sample_csv):
    """Test CSV ingestion with a valid file."""
    files = {"file": ("sample.csv", sample_csv, "text/csv")}
    response = client.post("/ingest/", files=files)

    assert response.status_code == 200
    assert response.json()["message"] == "Data ingested successfully"
    assert response.json()["rows"] > 0 

def test_ingest_invalid_csv():
    """Test CSV ingestion with an invalid file format."""
    files = {"file": ("sample.txt", io.BytesIO(b"Invalid content"), "text/plain")}
    response = client.post("/ingest/", files=files)

    assert response.status_code == 400
    assert "Exception at ingest_data" in response.text

def test_ingest_empty_csv():
    """Test ingestion of an empty CSV file."""
    empty_csv = io.BytesIO(b"")  
    files = {"file": ("empty.csv", empty_csv, "text/csv")}
    response = client.post("/ingest/", files=files)

    assert response.status_code == 400
    assert "No columns to parse" in response.text  
import sqlite3
import pytest
from fastapi.testclient import TestClient
import sys
import os
import io
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..","app")))
from app.main import app



client = TestClient(app)

def test_health_check():
    """Basic test to check if API is running."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message":"Welcome to the Customer Support Insights API!"}


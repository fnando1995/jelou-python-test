from fastapi.testclient import TestClient
from app.main import app
import jwt
from app.config import settings

client = TestClient(app)

# Generate a valid token for testing
test_payload = {"sub": "testuser"}
test_token = jwt.encode(test_payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
auth_header = {"Authorization": f"Bearer {test_token}"}

def test_root_endpoints():
    # Without data loaded, the insights endpoint should error out.
    response = client.get("/companies/test/insights", headers=auth_header)
    assert response.status_code == 400

def test_ingest_and_insights():
    # Create a simple CSV for testing data ingestion
    csv_content = """tweet_id,author_id,inbound,created_at,text,response_tweet_id,in_response_to_tweet_id
1,company1,True,2023-03-20 10:00:00,"Issue with product",2,
2,company1,False,2023-03-20 10:05:00,"Response to issue",,
"""
    files = {"file": ("test.csv", csv_content, "text/csv")}
    response = client.post("/ingest/", files=files)
    assert response.status_code == 200

    response = client.get("/companies/company1/insights", headers=auth_header)
    assert response.status_code == 200
    data = response.json()
    assert "total_inbound" in data

def test_ai_insights():
    response = client.get("/companies/company1/ai-insights", headers=auth_header)
    # Depending on whether data is loaded, this might error.
    if response.status_code == 400:
        assert "Dataset not loaded" in response.json()["detail"]
    else:
        data = response.json()
        assert "insights" in data

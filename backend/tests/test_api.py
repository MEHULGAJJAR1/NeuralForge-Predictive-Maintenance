from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_summary():
    response = client.get("/api/summary")
    assert response.status_code == 200

def test_analysis():
    response = client.post("/api/analyze", json={"vibration":4.8,"temperature_c":92,"pressure":8.2})
    assert response.status_code == 200

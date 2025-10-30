from fastapi.testclient import TestClient
from db import SessionLocal, Job, Base, engine
from main import app

# NEW: reset the database before each test
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_webhook_creates_job():
    response = client.post("/webhook", json={"path": "/test/video.mkv"})
    assert response.status_code == 200
    data = response.json()
    assert data["path"] == "/test/video.mkv"
    assert data["status"] == "pending"

def test_worker_gets_next_job():
    response = client.get("/job/next")
    assert response.status_code == 200
    data = response.json()
    assert data["path"] == "/test/video.mkv"
    assert data["status"] == "processing"

def test_worker_updates_job():
    # Update job id 1 to complete
    response = client.patch("/job/1", json={"status": "complete"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "complete"
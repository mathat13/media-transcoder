from fastapi.testclient import TestClient
from main import app
from conftest import TestingSessionLocal
from factories import JobFactory

client = TestClient(app)


def test_worker_updates_job(db_session):
    job = JobFactory(status="processing")

    response = client.patch(f"/job/{job.id}", json={"status": "complete"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "complete"

def test_worker_gets_next_job(db_session):
    job = JobFactory()
    response = client.get("/job/next")
    assert response.status_code == 200
    data = response.json()
    assert data["path"] == job.path
    assert data["status"] == "processing"

def test_webhook_creates_job(db_session):
    response = client.post("/webhook", json={"path": "/test/video.mkv"})
    assert response.status_code == 200
    data = response.json()
    assert data["path"] == "/test/video.mkv"
    assert data["status"] == "pending"
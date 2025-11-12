from fastapi.testclient import TestClient
from main import app
from tests.conftest import TestingSessionLocal
from src.factories import JobFactory, RadarrWebhookPayloadFactory, SonarrWebhookPayloadFactory

client = TestClient(app)

def test_radarr_webhook_creates_job(db_session):
    payload = RadarrWebhookPayloadFactory()

    response = client.post(
        "/webhook/radarr",
        json=payload.model_dump()
    )

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "pending"
    assert data["path"] in payload.movieFile.path

def test_sonarr_webhook_creates_job(db_session):
    payload = SonarrWebhookPayloadFactory()

    response = client.post(
        "/webhook/sonarr",
        json=payload.model_dump()
    )

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "pending"
    assert data["path"] in payload.episodeFile.path
    
def test_worker_updates_job(db_session):
    job = JobFactory(status="processing")

    response = client.patch(f"/job/{job.id}", json={"status": "complete"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "complete"

def test_worker_gets_next_job(db_session):
    job = JobFactory()
    # jobs = db_session.query(Job).all()
    # print(f"DB contains: {[j.path for j in jobs]}")
    response = client.get("/job/next")
    assert response.status_code == 200
    data = response.json()
    assert data["path"] == job.path
    assert data["status"] == "processing"
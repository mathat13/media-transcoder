from fastapi.testclient import TestClient
from main import app
from tests.conftest import TestingSessionLocal
from src.factories import JobFactory, JobValidationRequestFactory, RadarrWebhookPayloadFactory, SonarrWebhookPayloadFactory
from src.JobService import JobService
from src.db import Job

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
    source_path = "/path/to/media/file.mkv"
    print(db_session.query(Job).all())
    job = JobService(db_session).add_job(source_path)
    job = JobService(db_session).get_next_pending_job()

    assert job.status == "processing"
    assert job.output_path is not None
    assert isinstance(job, Job)

    validation_payload = JobValidationRequestFactory(output_path=job.output_path)
    print(f"Validation payload: {validation_payload.model_dump()}")
    assert validation_payload.output_path == job.output_path

    response = client.patch(f"/job/{job.id}", json=validation_payload.model_dump())

    assert response.status_code == 200

    data = response.json()
    
    assert data["status"] == "done"
    assert data["output_path"] == job.output_path == validation_payload.output_path
    assert data["id"] == job.id

def test_worker_gets_next_job(db_session):
    job = JobFactory()
    # jobs = db_session.query(Job).all()
    # print(f"DB contains: {[j.path for j in jobs]}")
    response = client.get("/job/next")
    assert response.status_code == 200
    data = response.json()
    assert data["source_path"] == job.source_path
    assert data["output_path"] == job.output_path
    assert data["status"] == "processing"

def test_JobService_validate_job(db_session):
    source_path = "/path/to/media/file.mkv"
    job = JobService(db_session).add_job(source_path)
    job = JobService(db_session).get_next_pending_job()
    output_path = job.output_path
    validated_job = JobService(db_session).validate_job(job.id, output_path)

    assert validated_job.status == "done"
    assert validated_job.output_path == output_path
    assert validated_job.id == job.id

def test_JobService_add_job(db_session):
    source_path = "/path/to/media/file.mkv"

    job_response = JobService(db_session).add_job(source_path)
    assert job_response.source_path == source_path
    assert job_response.status == "pending"
    assert job_response.id is not None
    assert isinstance(job_response, Job)

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional, List

from src.db import SessionLocal, Job
from src.JobService import JobService, JobResponse, JobStatus
from src.schemas.radarr import RadarrWebhookPayload
from src.schemas.sonarr import SonarrWebhookPayload

# Pydantic models\

class JobUpdate(BaseModel):
    status: Optional[str] = None
    path: Optional[str] = None

app = FastAPI()

# Dependency to get db session
def get_db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@app.post("/webhook/radarr", response_model=JobResponse)
def webhook_listener(payload: RadarrWebhookPayload, db: Session = Depends(get_db_session)):
    """
    Receives Radarr webhook → inserts into SQLite job table
    """

    # Only act on movie downloads
    if payload.eventType != "Download":
        raise HTTPException(status_code=204, detail="Ignoring event")
    
    movie_path = payload.movieFile.path

    # Check if job already exists (prevents duplicates)
    existing = db.query(Job).filter(Job.path == movie_path).first()
    if existing:
        raise HTTPException(status_code=400, detail="Job already exists")

    # Create and save the new job
    new_job = Job(job_type="movie", source_path=movie_path, status="pending")
    db.add(new_job)
    db.commit()
    db.refresh(new_job)  # refresh gets the auto-generated job ID

    return JobResponse(
        id=new_job.id,
        path=new_job.path,
        status=new_job.status
    )

@app.post("/webhook/sonarr", response_model=JobResponse)
def webhook_listener(payload: SonarrWebhookPayload, db: Session = Depends(get_db_session)):
    """
    Receives Sonarr webhook → inserts into SQLite job table
    """

    # Only act on import downloads
    if payload.eventType != "Download":
        raise HTTPException(status_code=204, detail="Ignoring event")
    
    episode_path = payload.episodeFile.path

    # Check if job already exists (prevents duplicates)
    existing = db.query(Job).filter(Job.path == episode_path).first()
    if existing:
        raise HTTPException(status_code=400, detail="Job already exists")

    # Create and save the new job
    new_job = Job(path=episode_path, status="pending")
    db.add(new_job)
    db.commit()
    db.refresh(new_job)  # refresh gets the auto-generated job ID

    return JobResponse(
        id=new_job.id,
        path=new_job.path,
        status=new_job.status
    )


@app.get("/job/next", response_model=JobResponse)
def get_next_job(db: Session = Depends(get_db_session)):
    return JobService(db).get_next_pending_job()
    
@app.patch("/job/{job_id}", response_model=JobResponse)
def patch_job(job_id: int, update: JobUpdate, db: Session = Depends(get_db_session)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if update.status is not None:
        job.status = update.status

    if update.path is not None:
        job.path = update.path
    
    db.commit()
    db.refresh(job)

    return JobResponse(
        id=job.id,
        path=job.path,
        status=job.status
    )

# Add database deletion api call here

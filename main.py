from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional
from db import SessionLocal, Job

app = FastAPI()

# Pydantic models\
class WebhookPayload(BaseModel):
    path: str

class JobResponse(BaseModel):
    id: int
    path: str
    status: str

class JobUpdate(BaseModel):
    status: Optional[str] = None
    path: Optional[str] = None

# Dependency to get db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/webhook", response_model=JobResponse)
def webhook_listener(payload: WebhookPayload, db: Session = Depends(get_db)):
    """
    Receives Radarr webhook → inserts into SQLite job table
    """
    # Check if job already exists (prevents duplicates)
    existing = db.query(Job).filter(Job.path == payload.path).first()
    if existing:
        raise HTTPException(status_code=400, detail="Job already exists")

    # Create and save the new job
    new_job = Job(path=payload.path, status="pending")
    db.add(new_job)
    db.commit()
    db.refresh(new_job)  # refresh gets the auto-generated job ID

    return JobResponse(
        id=new_job.id,
        path=new_job.path,
        status=new_job.status
    )

@app.get("/job/next" , response_model=JobResponse)
def get_next_job(db: Session = Depends(get_db)):
    # Query for the next pending job
    next_job = db.query(Job).filter(Job.status == "pending").order_by(Job.created_at.asc()).first()

    # Return error if no pending jobs
    if next_job is None:
        raise HTTPException(status_code=404, detail="No pending jobs available")
    
    # Update job status to processing
    setattr(next_job, 'status', 'processing')
    db.commit()
    db.refresh(next_job)

    return JobResponse(
        id=next_job.id,
        path=next_job.path,
        status=next_job.status
    )
    
@app.patch("/job/{job_id}", response_model=JobResponse)
def patch_job(job_id: int, update: JobUpdate, db: Session = Depends(get_db)):
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
# Will need to integrate with jellyfin and radarr to assure that database deletion is safe
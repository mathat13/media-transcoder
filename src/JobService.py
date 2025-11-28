import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException
from pydantic import BaseModel
from typing import Optional
from enum import Enum
from os import path

from src.db import Job

JOB_STATE_MACHINE = {
    "staged": ["pending"],
    "pending": ["processing"],
    "processing": ["validating", "failed"],
    "validating": ["done", "failed"],
    "done": [],
    "failed": [],
}

class JobStatus(str, Enum):
    staged = "staged"
    pending = "pending"
    processing = "processing"
    validating = "validating"
    done = "done"
    failed = "failed"

class JobResponse(BaseModel):
    id: int
    source_path: str
    output_path: str
    status: JobStatus

    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None

    error_message: Optional[str] = None
    worker_notes: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

class JobValidationRequest(BaseModel):
    output_path: str
    
class JobValidator:
    def validate(self, job: Job) -> bool:
        # Hook where real validation will eventually go
        return True

class JobService:
    def __init__(self, db: Session):
        self.db = db

    def _get_job_by_id(self, job_id: int):
        """Retrieve a job by its ID."""
        job = self.db.query(Job).filter(Job.id == job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return job
    
    def save_job(self, job: Job) -> Job:
        """Persist a Job to the database."""
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job
    
    def create_job(self, source_path: str, job_type: str = "episode") -> Job:
        """Create a Job domain object (does not persist)."""
        return Job(
            source_path=source_path,
            output_path=path.join("apple", source_path), # Dummy output path
            job_type=job_type,
            status="pending",
        )

    def add_job(self, source_path: str) -> Job:
        """Add a new job to the database."""
        # Check for existing job with same source path
        existing = self.db.query(Job).filter(Job.source_path == source_path).first()
        if existing:
            raise HTTPException(status_code=400, detail="Job already exists")
        
        # Create new job object with source path and initial pending status
        new_job = self.create_job(source_path=source_path)
        return self.save_job(new_job)

    def get_next_pending_job(self):
        """Return the oldest pending job and mark it as processing."""
        job = (
            self.db.query(Job)
            .filter(Job.status == "pending")
            .order_by(Job.created_at.asc())
            .first()
        )
        if not job:
            raise HTTPException(status_code=404, detail="No pending jobs")

        return self._transition(job, "processing")

    def validate_job(self, job_id: int, output_path: str):
        """Mark job as processing → validating."""
        job = self._get_job_by_id(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        self._transition(job, "validating")

        valid = JobValidator().validate(job)
        if not valid:
            return self._transition(job, "failed")
        else:
            return self._transition(job, "done")
        
    def complete_job(self, job_id: int):
        """Mark job as validating → done if successful."""
        job = self.db.query(Job).filter(Job.id == job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")

        return self._transition(job, "validating")

    def fail_job(self, job_id: int):
        """Mark job as failed from any state."""
        job = self.db.query(Job).filter(Job.id == job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")

        return self._transition(job, "failed")

    def _transition(self, job: Job, new_status: str):
        """Internal helper to safely change job status."""
        allowed = JOB_STATE_MACHINE.get(job.status, [])
        if new_status not in allowed:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid transition {job.status} → {new_status}",
            )

        job.status = new_status
        job.updated_at = datetime.datetime.now(datetime.timezone.utc)
        self.db.commit()
        self.db.refresh(job)
        return job
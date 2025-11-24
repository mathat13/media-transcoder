import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException
from pydantic import BaseModel
from typing import Optional
from enum import Enum

from src.db import Job

JOB_STATE_MACHINE = {
    "pending": ["processing"],
    "processing": ["validating", "failed"],
    "validating": ["done", "failed"],
    "done": [],
    "failed": [],
}

class JobStatus(str, Enum):
    pending = "pending"
    processing = "processing"
    validating = "validating"
    completed = "completed"
    failed = "failed"

class JobResponse(BaseModel):
    id: int
    source_path: str
    status: JobStatus

    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None

    error_message: Optional[str] = None
    worker_notes: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

class JobService:
    def __init__(self, db: Session):
        self.db = db

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
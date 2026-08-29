from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models.user import User
from app.schemas.job import (
    JobCreateSchema,
    JobUpdateSchema,
    JobStatusUpdateSchema,
    JobResponseSchema,
)
from app.services.job_service import JobService
from app.utils.auth import require_admin, get_current_user

router = APIRouter(prefix="/api/jobs", tags=["jobs"])


@router.post("", response_model=JobResponseSchema, status_code=201)
def create_job(
    data: JobCreateSchema,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    service = JobService(db)
    job = service.create_job(admin.id, data)
    return job


@router.get("")
def search_jobs(
    skill: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
    experience_level: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db),
):
    service = JobService(db)
    result = service.search_jobs(
        skill=skill,
        location=location,
        experience_level=experience_level,
        page=page,
    )
    return result


@router.get("/{job_id}", response_model=JobResponseSchema)
def get_job(job_id: int, db: Session = Depends(get_db)):
    service = JobService(db)
    return service.get_job(job_id)


@router.put("/{job_id}", response_model=JobResponseSchema)
def update_job(
    job_id: int,
    data: JobUpdateSchema,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    service = JobService(db)
    return service.update_job(admin.id, job_id, data)


@router.patch("/{job_id}/status", response_model=JobResponseSchema)
def update_job_status(
    job_id: int,
    data: JobStatusUpdateSchema,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    service = JobService(db)
    return service.update_status(admin.id, job_id, data.status.value)

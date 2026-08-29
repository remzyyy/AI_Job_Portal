from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.application import ApplicationStatusUpdateSchema, ApplicationResponseSchema
from app.services.application_service import ApplicationService
from app.utils.auth import require_admin, require_candidate

router = APIRouter(prefix="/api", tags=["applications"])


@router.post("/jobs/{job_id}/apply", status_code=201)
def apply_to_job(
    job_id: int,
    candidate: User = Depends(require_candidate),
    db: Session = Depends(get_db),
):
    service = ApplicationService(db)
    application = service.apply(candidate.id, job_id)
    return {
        "id": application.id,
        "status": application.status,
        "job_id": application.job_id,
        "message": "Application submitted successfully",
    }


@router.get("/jobs/{job_id}/applications")
def get_job_applications(
    job_id: int,
    page: int = Query(1, ge=1),
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    service = ApplicationService(db)
    result = service.get_applications_for_job(admin.id, job_id, page)

    # Enrich with candidate info
    from app.models.candidate_profile import CandidateProfile

    items = []
    for app in result["items"]:
        profile = db.query(CandidateProfile).filter(
            CandidateProfile.candidate_id == app.candidate_id
        ).first()
        items.append({
            "id": app.id,
            "candidate_id": app.candidate_id,
            "job_id": app.job_id,
            "status": app.status,
            "applied_at": app.applied_at.isoformat() if app.applied_at else None,
            "candidate_name": profile.name if profile else "Unknown",
            "candidate_skills": profile.skills if profile else [],
        })

    return {
        "items": items,
        "total": result["total"],
        "page": result["page"],
        "total_pages": result["total_pages"],
    }


@router.patch("/applications/{application_id}/status")
def update_application_status(
    application_id: int,
    data: ApplicationStatusUpdateSchema,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    service = ApplicationService(db)
    application = service.update_status(admin.id, application_id, data.status.value)
    return {
        "id": application.id,
        "status": application.status,
        "message": "Application status updated",
    }


@router.get("/candidates/applications")
def get_my_applications(
    page: int = Query(1, ge=1),
    candidate: User = Depends(require_candidate),
    db: Session = Depends(get_db),
):
    service = ApplicationService(db)
    result = service.get_candidate_applications(candidate.id, page)

    from app.models.job_listing import JobListing

    items = []
    for app in result["items"]:
        job = db.query(JobListing).filter(JobListing.id == app.job_id).first()
        items.append({
            "id": app.id,
            "job_id": app.job_id,
            "job_title": job.title if job else "Unknown",
            "status": app.status,
            "applied_at": app.applied_at.isoformat() if app.applied_at else None,
        })

    return {
        "items": items,
        "total": result["total"],
        "page": result["page"],
        "total_pages": result["total_pages"],
    }

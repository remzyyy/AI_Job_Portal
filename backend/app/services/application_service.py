from sqlalchemy.orm import Session

from app.models.application import Application
from app.models.job_listing import JobListing
from app.models.candidate_profile import CandidateProfile
from app.utils.exceptions import (
    NotFoundError,
    AuthorizationError,
    ValidationError,
    ConflictError,
)
from app.utils.pagination import paginate


class ApplicationService:
    def __init__(self, db: Session):
        self.db = db

    def apply(self, candidate_id: int, job_id: int) -> Application:
        # Check candidate has a profile
        profile = self.db.query(CandidateProfile).filter(
            CandidateProfile.candidate_id == candidate_id
        ).first()
        if not profile:
            raise ValidationError("You must create a profile before applying to jobs")

        # Check job exists and is open
        job = self.db.query(JobListing).filter(JobListing.id == job_id).first()
        if not job:
            raise NotFoundError("JobListing", job_id)
        if job.status != "open":
            raise ValidationError("This job listing is no longer accepting applications")

        # Check for duplicate application
        existing = self.db.query(Application).filter(
            Application.candidate_id == candidate_id,
            Application.job_id == job_id,
        ).first()
        if existing:
            raise ConflictError("You have already applied to this job listing")

        application = Application(
            candidate_id=candidate_id,
            job_id=job_id,
            status="Applied",
        )
        self.db.add(application)
        self.db.commit()
        self.db.refresh(application)
        return application

    def get_applications_for_job(self, admin_id: int, job_id: int, page: int = 1) -> dict:
        job = self.db.query(JobListing).filter(JobListing.id == job_id).first()
        if not job:
            raise NotFoundError("JobListing", job_id)
        if job.admin_id != admin_id:
            raise AuthorizationError()

        query = (
            self.db.query(Application)
            .filter(Application.job_id == job_id)
            .order_by(Application.applied_at.desc())
        )
        return paginate(query, page)

    def update_status(self, admin_id: int, application_id: int, status: str) -> Application:
        application = self.db.query(Application).filter(
            Application.id == application_id
        ).first()
        if not application:
            raise NotFoundError("Application", application_id)

        # Verify admin owns the job
        job = self.db.query(JobListing).filter(JobListing.id == application.job_id).first()
        if job.admin_id != admin_id:
            raise AuthorizationError()

        valid_statuses = ("Applied", "Shortlisted", "Rejected")
        if status not in valid_statuses:
            raise ValidationError(
                f"Status must be one of: {', '.join(valid_statuses)}", field="status"
            )

        application.status = status
        self.db.commit()
        self.db.refresh(application)
        return application

    def get_candidate_applications(self, candidate_id: int, page: int = 1) -> dict:
        query = (
            self.db.query(Application)
            .filter(Application.candidate_id == candidate_id)
            .order_by(Application.applied_at.desc())
        )
        return paginate(query, page)

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.job_listing import JobListing
from app.schemas.job import JobCreateSchema, JobUpdateSchema, JobStatus
from app.utils.exceptions import NotFoundError, AuthorizationError, ValidationError
from app.utils.pagination import paginate


class JobService:
    def __init__(self, db: Session):
        self.db = db

    def create_job(self, admin_id: int, data: JobCreateSchema) -> JobListing:
        job = JobListing(
            admin_id=admin_id,
            title=data.title,
            description=data.description,
            required_skills=data.required_skills,
            experience_level=data.experience_level.value,
            location=data.location,
            status="open",
        )
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job

    def update_job(self, admin_id: int, job_id: int, data: JobUpdateSchema) -> JobListing:
        job = self._get_job_or_404(job_id)
        self._check_ownership(job, admin_id)

        update_data = data.model_dump(exclude_unset=True)
        if "experience_level" in update_data and update_data["experience_level"]:
            update_data["experience_level"] = update_data["experience_level"].value

        for field, value in update_data.items():
            setattr(job, field, value)

        self.db.commit()
        self.db.refresh(job)
        return job

    def update_status(self, admin_id: int, job_id: int, status: str) -> JobListing:
        job = self._get_job_or_404(job_id)
        self._check_ownership(job, admin_id)

        if status not in ("open", "closed"):
            raise ValidationError("Status must be 'open' or 'closed'", field="status")

        job.status = status
        self.db.commit()
        self.db.refresh(job)
        return job

    def get_job(self, job_id: int) -> JobListing:
        return self._get_job_or_404(job_id)

    def search_jobs(
        self,
        skill: str = None,
        location: str = None,
        experience_level: str = None,
        page: int = 1,
    ) -> dict:
        query = self.db.query(JobListing).filter(JobListing.status == "open")

        if skill:
            # Case-insensitive skill matching in JSON array
            query = query.filter(
                func.lower(JobListing.required_skills).contains(func.lower(f'"{skill}"'))
            )

        if location:
            # Partial, case-insensitive match so "Mumbai" matches "Mumbai, India"
            # and "India" matches any Indian location.
            query = query.filter(JobListing.location.ilike(f"%{location}%"))

        if experience_level:
            query = query.filter(JobListing.experience_level == experience_level)

        query = query.order_by(JobListing.created_at.desc())
        return paginate(query, page)

    def _get_job_or_404(self, job_id: int) -> JobListing:
        job = self.db.query(JobListing).filter(JobListing.id == job_id).first()
        if not job:
            raise NotFoundError("JobListing", job_id)
        return job

    def _check_ownership(self, job: JobListing, admin_id: int):
        if job.admin_id != admin_id:
            raise AuthorizationError()

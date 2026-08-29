from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.application import Application
from app.models.job_listing import JobListing
from app.models.candidate_profile import CandidateProfile


class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db

    def get_dashboard(self, admin_id: int) -> dict:
        return {
            "applications_per_job": self.get_applications_per_job(admin_id),
            "skills_distribution": self.get_skills_distribution(admin_id),
            "status_breakdown": self.get_status_breakdown(admin_id),
        }

    def get_applications_per_job(self, admin_id: int) -> list:
        results = (
            self.db.query(
                JobListing.id,
                JobListing.title,
                func.count(Application.id).label("count"),
            )
            .outerjoin(Application, Application.job_id == JobListing.id)
            .filter(JobListing.admin_id == admin_id)
            .group_by(JobListing.id, JobListing.title)
            .all()
        )
        return [{"job_id": r[0], "title": r[1], "count": r[2]} for r in results]

    def get_skills_distribution(self, admin_id: int) -> list:
        # Get all candidate profiles that applied to this admin's jobs
        applications = (
            self.db.query(Application.candidate_id)
            .join(JobListing, JobListing.id == Application.job_id)
            .filter(JobListing.admin_id == admin_id)
            .distinct()
            .all()
        )
        candidate_ids = [a[0] for a in applications]

        if not candidate_ids:
            return []

        profiles = (
            self.db.query(CandidateProfile.skills)
            .filter(CandidateProfile.candidate_id.in_(candidate_ids))
            .all()
        )

        # Count skills
        skill_counts = {}
        for (skills,) in profiles:
            if skills:
                for skill in skills:
                    skill_lower = skill.lower()
                    skill_counts[skill_lower] = skill_counts.get(skill_lower, 0) + 1

        return [
            {"skill": skill, "count": count}
            for skill, count in sorted(skill_counts.items(), key=lambda x: -x[1])
        ]

    def get_status_breakdown(self, admin_id: int) -> dict:
        results = (
            self.db.query(Application.status, func.count(Application.id))
            .join(JobListing, JobListing.id == Application.job_id)
            .filter(JobListing.admin_id == admin_id)
            .group_by(Application.status)
            .all()
        )
        breakdown = {"Applied": 0, "Shortlisted": 0, "Rejected": 0}
        for status, count in results:
            breakdown[status] = count
        return breakdown

from sqlalchemy.orm import Session

from app.models.candidate_profile import CandidateProfile
from app.schemas.candidate import ProfileCreateSchema, ProfileUpdateSchema
from app.utils.exceptions import NotFoundError, ConflictError


class CandidateService:
    def __init__(self, db: Session):
        self.db = db

    def create_profile(self, candidate_id: int, data: ProfileCreateSchema) -> CandidateProfile:
        existing = self.db.query(CandidateProfile).filter(
            CandidateProfile.candidate_id == candidate_id
        ).first()
        if existing:
            raise ConflictError("A profile already exists for this candidate")

        profile = CandidateProfile(
            candidate_id=candidate_id,
            name=data.name,
            skills=data.skills,
            education=data.education,
            project_summaries=data.project_summaries,
            preferred_location=data.preferred_location,
            role_type=data.role_type,
            domain_interest=data.domain_interest,
        )
        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)
        return profile

    def update_profile(self, candidate_id: int, data: ProfileUpdateSchema) -> CandidateProfile:
        profile = self._get_profile_or_404(candidate_id)

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(profile, field, value)

        self.db.commit()
        self.db.refresh(profile)
        return profile

    def get_profile(self, candidate_id: int) -> CandidateProfile:
        return self._get_profile_or_404(candidate_id)

    def _get_profile_or_404(self, candidate_id: int) -> CandidateProfile:
        profile = self.db.query(CandidateProfile).filter(
            CandidateProfile.candidate_id == candidate_id
        ).first()
        if not profile:
            raise NotFoundError("CandidateProfile", candidate_id)
        return profile

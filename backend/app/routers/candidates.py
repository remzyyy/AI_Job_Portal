from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.candidate import (
    ProfileCreateSchema,
    ProfileUpdateSchema,
    ProfileResponseSchema,
)
from app.services.candidate_service import CandidateService
from app.utils.auth import require_candidate

router = APIRouter(prefix="/api/candidates", tags=["candidates"])


@router.post("/profile", response_model=ProfileResponseSchema, status_code=201)
def create_profile(
    data: ProfileCreateSchema,
    candidate: User = Depends(require_candidate),
    db: Session = Depends(get_db),
):
    service = CandidateService(db)
    return service.create_profile(candidate.id, data)


@router.get("/profile", response_model=ProfileResponseSchema)
def get_profile(
    candidate: User = Depends(require_candidate),
    db: Session = Depends(get_db),
):
    service = CandidateService(db)
    return service.get_profile(candidate.id)


@router.put("/profile", response_model=ProfileResponseSchema)
def update_profile(
    data: ProfileUpdateSchema,
    candidate: User = Depends(require_candidate),
    db: Session = Depends(get_db),
):
    service = CandidateService(db)
    return service.update_profile(candidate.id, data)

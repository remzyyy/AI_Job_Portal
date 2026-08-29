from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.matching import MatchQuerySchema
from app.services.matching_service import MatchingService
from app.utils.auth import require_candidate

router = APIRouter(prefix="/api/matching", tags=["matching"])


@router.post("")
def match_jobs(
    data: MatchQuerySchema,
    candidate: User = Depends(require_candidate),
    db: Session = Depends(get_db),
):
    service = MatchingService(db)
    return service.match(data.query)

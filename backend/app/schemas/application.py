from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class ApplicationStatus(str, Enum):
    APPLIED = "Applied"
    SHORTLISTED = "Shortlisted"
    REJECTED = "Rejected"


class ApplicationStatusUpdateSchema(BaseModel):
    status: ApplicationStatus


class ApplicationResponseSchema(BaseModel):
    id: int
    candidate_id: int
    job_id: int
    status: str
    applied_at: datetime
    updated_at: Optional[datetime] = None
    candidate_name: Optional[str] = None
    candidate_skills: Optional[list] = None

    class Config:
        from_attributes = True

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class ExperienceLevel(str, Enum):
    ENTRY = "Entry"
    MID = "Mid"
    SENIOR = "Senior"
    LEAD = "Lead"


class JobStatus(str, Enum):
    OPEN = "open"
    CLOSED = "closed"


class JobCreateSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=150)
    description: str = Field(..., min_length=1, max_length=5000)
    required_skills: List[str] = Field(..., min_length=1, max_length=20)
    experience_level: ExperienceLevel
    location: str = Field(..., min_length=1)


class JobUpdateSchema(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=150)
    description: Optional[str] = Field(None, min_length=1, max_length=5000)
    required_skills: Optional[List[str]] = Field(None, min_length=1, max_length=20)
    experience_level: Optional[ExperienceLevel] = None
    location: Optional[str] = Field(None, min_length=1)


class JobStatusUpdateSchema(BaseModel):
    status: JobStatus


class JobResponseSchema(BaseModel):
    id: int
    admin_id: int
    title: str
    description: str
    required_skills: List[str]
    experience_level: str
    location: str
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class JobFilterSchema(BaseModel):
    skill: Optional[str] = None
    location: Optional[str] = None
    experience_level: Optional[ExperienceLevel] = None
    page: int = Field(1, ge=1)

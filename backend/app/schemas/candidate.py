from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ProfileCreateSchema(BaseModel):
    name: str = Field(..., min_length=1)
    skills: List[str] = Field(..., min_length=1, max_length=50)
    education: List[str] = Field(..., min_length=1, max_length=20)
    project_summaries: List[str] = Field(default_factory=list, max_length=20)
    preferred_location: Optional[str] = Field(None, max_length=200)
    role_type: Optional[str] = Field(None, max_length=200)
    domain_interest: Optional[str] = Field(None, max_length=200)


class ProfileUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    skills: Optional[List[str]] = Field(None, min_length=1, max_length=50)
    education: Optional[List[str]] = Field(None, min_length=1, max_length=20)
    project_summaries: Optional[List[str]] = Field(None, max_length=20)
    preferred_location: Optional[str] = Field(None, max_length=200)
    role_type: Optional[str] = Field(None, max_length=200)
    domain_interest: Optional[str] = Field(None, max_length=200)


class ProfileResponseSchema(BaseModel):
    id: int
    candidate_id: int
    name: str
    skills: List[str]
    education: List[str]
    project_summaries: List[str]
    preferred_location: Optional[str] = None
    role_type: Optional[str] = None
    domain_interest: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

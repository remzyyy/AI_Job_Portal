from typing import List, Optional

from pydantic import BaseModel, Field


class MatchQuerySchema(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000)


class MatchResultSchema(BaseModel):
    job_id: int
    title: str
    score: int = Field(..., ge=0, le=100)
    explanation: str


class MatchResponseSchema(BaseModel):
    results: List[MatchResultSchema]
    message: Optional[str] = None

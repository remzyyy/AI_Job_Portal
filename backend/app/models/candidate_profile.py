from datetime import datetime

from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class CandidateProfile(Base):
    __tablename__ = "candidate_profiles"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    name = Column(String, nullable=False)
    skills = Column(JSON, nullable=False)  # list of strings, 1-50 items
    education = Column(JSON, nullable=False)  # list of strings, 1-20 entries
    project_summaries = Column(JSON, default=list)  # list of strings, 0-20 entries
    preferred_location = Column(String(200), nullable=True)
    role_type = Column(String(200), nullable=True)
    domain_interest = Column(String(200), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    candidate = relationship("User", backref="profile")

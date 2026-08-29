from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class JobListing(Base):
    __tablename__ = "job_listings"

    id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    required_skills = Column(JSON, nullable=False)  # list of strings
    experience_level = Column(String, nullable=False)  # Entry, Mid, Senior, Lead
    location = Column(String, nullable=False)
    status = Column(String, default="open")  # open or closed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    admin = relationship("User", backref="job_listings")
    applications = relationship("Application", back_populates="job")

"""Feature: ai-job-board — Property-based tests for application business rules."""
import pytest
from hypothesis import given, strategies as st, settings, HealthCheck

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.models.user import User
from app.models.job_listing import JobListing
from app.models.candidate_profile import CandidateProfile
from app.services.application_service import ApplicationService
from app.utils.auth import hash_password
from app.utils.exceptions import ValidationError, ConflictError


def _fresh_db():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine)()


def _setup(db, with_profile=True, job_status="open"):
    admin = User(email="a@t.com", password_hash=hash_password("pw"), role="admin")
    cand = User(email="c@t.com", password_hash=hash_password("pw"), role="candidate")
    db.add_all([admin, cand])
    db.commit()
    db.refresh(admin)
    db.refresh(cand)

    if with_profile:
        profile = CandidateProfile(
            candidate_id=cand.id, name="Jane", skills=["Python"], education=["BS"],
            project_summaries=[],
        )
        db.add(profile)

    job = JobListing(
        admin_id=admin.id, title="Engineer", description="desc",
        required_skills=["Python"], experience_level="Mid", location="Remote",
        status=job_status,
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return admin, cand, job


# Property 9: Applications to closed listings are rejected
# Validates: Requirements 4.3

def test_apply_to_closed_listing_rejected():
    db = _fresh_db()
    try:
        _, cand, job = _setup(db, job_status="closed")
        service = ApplicationService(db)
        with pytest.raises(ValidationError):
            service.apply(cand.id, job.id)
    finally:
        db.close()


# Property 10: Duplicate applications are rejected
# Validates: Requirements 4.4

def test_duplicate_application_rejected():
    db = _fresh_db()
    try:
        _, cand, job = _setup(db)
        service = ApplicationService(db)
        service.apply(cand.id, job.id)
        with pytest.raises(ConflictError):
            service.apply(cand.id, job.id)
    finally:
        db.close()


# Property 11: Applications require a candidate profile
# Validates: Requirements 4.5

def test_apply_without_profile_rejected():
    db = _fresh_db()
    try:
        _, cand, job = _setup(db, with_profile=False)
        service = ApplicationService(db)
        with pytest.raises(ValidationError):
            service.apply(cand.id, job.id)
    finally:
        db.close()


# Successful application sets status "Applied"
def test_successful_application_status():
    db = _fresh_db()
    try:
        _, cand, job = _setup(db)
        service = ApplicationService(db)
        app = service.apply(cand.id, job.id)
        assert app.status == "Applied"
        assert app.candidate_id == cand.id
        assert app.job_id == job.id
    finally:
        db.close()

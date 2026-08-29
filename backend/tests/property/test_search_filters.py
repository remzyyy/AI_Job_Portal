"""Feature: ai-job-board — Property-based tests for search/filter and ownership."""
import pytest
from hypothesis import given, strategies as st, settings, HealthCheck

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.models.user import User
from app.models.job_listing import JobListing
from app.services.job_service import JobService
from app.schemas.job import JobUpdateSchema
from app.utils.auth import hash_password
from app.utils.exceptions import AuthorizationError


def _fresh_db():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine)()


def _admin(db, email="a@t.com"):
    u = User(email=email, password_hash=hash_password("pw"), role="admin")
    db.add(u)
    db.commit()
    db.refresh(u)
    return u


# Property 15: Search only includes open listings
# Validates: Requirements 7.5

def test_search_excludes_closed_listings():
    db = _fresh_db()
    try:
        admin = _admin(db)
        db.add(JobListing(admin_id=admin.id, title="Open Job", description="d",
                          required_skills=["Python"], experience_level="Mid",
                          location="Remote", status="open"))
        db.add(JobListing(admin_id=admin.id, title="Closed Job", description="d",
                          required_skills=["Python"], experience_level="Mid",
                          location="Remote", status="closed"))
        db.commit()
        service = JobService(db)
        result = service.search_jobs(page=1)
        titles = [j.title for j in result["items"]]
        assert "Open Job" in titles
        assert "Closed Job" not in titles
    finally:
        db.close()


# Property 14: Location filter is case-insensitive
# Validates: Requirements 7.2

@settings(max_examples=50, suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(case=st.sampled_from(["remote", "REMOTE", "Remote", "ReMoTe"]))
def test_location_filter_case_insensitive(case):
    db = _fresh_db()
    try:
        admin = _admin(db, email=f"a{id(db)}@t.com")
        db.add(JobListing(admin_id=admin.id, title="Job", description="d",
                          required_skills=["Python"], experience_level="Mid",
                          location="Remote", status="open"))
        db.commit()
        service = JobService(db)
        result = service.search_jobs(location=case, page=1)
        assert len(result["items"]) == 1
    finally:
        db.close()


# Property 16: results ordered by creation date descending
# Validates: Requirements 7.8

def test_search_ordered_by_created_desc():
    import time
    db = _fresh_db()
    try:
        admin = _admin(db)
        for i in range(3):
            db.add(JobListing(admin_id=admin.id, title=f"Job {i}", description="d",
                              required_skills=["Python"], experience_level="Mid",
                              location="Remote", status="open"))
            db.commit()
            time.sleep(0.01)
        service = JobService(db)
        result = service.search_jobs(page=1)
        created = [j.created_at for j in result["items"]]
        assert created == sorted(created, reverse=True)
    finally:
        db.close()


# Property 17: pagination structure
# Validates: Requirements 8.7

def test_pagination_structure():
    db = _fresh_db()
    try:
        admin = _admin(db)
        for i in range(25):
            db.add(JobListing(admin_id=admin.id, title=f"Job {i}", description="d",
                              required_skills=["Python"], experience_level="Mid",
                              location="Remote", status="open"))
        db.commit()
        service = JobService(db)
        result = service.search_jobs(page=1)
        assert len(result["items"]) <= 20
        assert result["total"] == 25
        assert result["page"] == 1
        assert result["total_pages"] == 2
    finally:
        db.close()


# Property 2: Job ownership authorization
# Validates: Requirements 1.7

def test_edit_job_not_owned_rejected():
    db = _fresh_db()
    try:
        owner = _admin(db, email="owner@t.com")
        other = _admin(db, email="other@t.com")
        job = JobListing(admin_id=owner.id, title="Job", description="d",
                         required_skills=["Python"], experience_level="Mid",
                         location="Remote", status="open")
        db.add(job)
        db.commit()
        db.refresh(job)
        service = JobService(db)
        with pytest.raises(AuthorizationError):
            service.update_job(other.id, job.id, JobUpdateSchema(title="Hacked"))
        with pytest.raises(AuthorizationError):
            service.update_status(other.id, job.id, "closed")
    finally:
        db.close()

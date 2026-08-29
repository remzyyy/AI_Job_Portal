"""Feature: ai-job-board — Property-based tests for AI matching structure."""
import pytest
from hypothesis import given, strategies as st, settings, HealthCheck

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.models.user import User
from app.models.job_listing import JobListing
from app.services.matching_service import MatchingService
from app.utils.auth import hash_password
from app.utils.exceptions import ValidationError


def _fresh_db():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine)()


def _seed_jobs(db, n_open=5, n_closed=2):
    admin = User(email="a@t.com", password_hash=hash_password("pw"), role="admin")
    db.add(admin)
    db.commit()
    db.refresh(admin)
    for i in range(n_open):
        db.add(JobListing(
            admin_id=admin.id, title=f"Python Engineer {i}", description="python backend remote healthcare",
            required_skills=["Python", "FastAPI"], experience_level="Mid", location="Remote", status="open",
        ))
    for i in range(n_closed):
        db.add(JobListing(
            admin_id=admin.id, title=f"Closed Python {i}", description="python backend",
            required_skills=["Python"], experience_level="Mid", location="Remote", status="closed",
        ))
    db.commit()


# Property 8: Whitespace-only queries are rejected
# Validates: Requirements 3.4

@settings(max_examples=100)
@given(query=st.text(alphabet=" \t\n\r", min_size=1, max_size=20))
def test_whitespace_only_query_rejected(query):
    db = _fresh_db()
    try:
        _seed_jobs(db)
        service = MatchingService(db)
        with pytest.raises(ValidationError):
            service.match(query)
    finally:
        db.close()


def test_empty_query_rejected():
    db = _fresh_db()
    try:
        _seed_jobs(db)
        service = MatchingService(db)
        with pytest.raises(ValidationError):
            service.match("")
    finally:
        db.close()


# Property: queries over 1000 chars rejected
# Validates: Requirements 3.5

def test_over_length_query_rejected():
    db = _fresh_db()
    try:
        _seed_jobs(db)
        service = MatchingService(db)
        with pytest.raises(ValidationError):
            service.match("x" * 1001)
    finally:
        db.close()


# Property 6: results are bounded, scored 0-100, ordered by score desc
# Property 7: only open listings returned
# Validates: Requirements 3.1, 3.2, 3.3

@settings(max_examples=50, suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(query=st.text(min_size=1, max_size=200).filter(lambda x: x.strip()))
def test_match_results_structure(query):
    db = _fresh_db()
    try:
        _seed_jobs(db, n_open=25, n_closed=5)  # more than 20 open
        # capture the set of open job IDs
        open_ids = {j.id for j in db.query(JobListing).filter(JobListing.status == "open").all()}
        service = MatchingService(db)
        result = service.match(query)
        results = result["results"]

        # At most 20
        assert len(results) <= 20

        # Each score in [0, 100]; only open listings; explanation non-empty
        prev = 101
        for r in results:
            assert 0 <= r["score"] <= 100
            assert r["job_id"] in open_ids  # never a closed listing
            assert r["explanation"]
            # Ordered by score descending
            assert r["score"] <= prev
            prev = r["score"]
    finally:
        db.close()

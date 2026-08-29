"""Feature: ai-job-board — Property-based tests for candidate profile management."""
import pytest
from hypothesis import given, strategies as st, settings, HealthCheck

from app.schemas.candidate import ProfileCreateSchema, ProfileUpdateSchema
from app.services.candidate_service import CandidateService
from app.models.user import User
from app.utils.exceptions import ConflictError
from app.utils.auth import hash_password
from pydantic import ValidationError as PydanticValidationError

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.database import Base


def _fresh_db():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine)()


def _make_candidate(db):
    user = User(email=f"c{id(db)}@t.com", password_hash=hash_password("pw"), role="candidate")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# Property 4: Profile validation rejects missing required fields
# Validates: Requirements 2.4

def test_missing_name_rejected():
    with pytest.raises(PydanticValidationError):
        ProfileCreateSchema(name="", skills=["Python"], education=["BS"])


def test_zero_skills_rejected():
    with pytest.raises(PydanticValidationError):
        ProfileCreateSchema(name="Jane", skills=[], education=["BS"])


# Property 3: Profile partial update preserves unmodified fields
# Validates: Requirements 2.2

@settings(max_examples=50, suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(new_name=st.text(min_size=1, max_size=50).filter(lambda x: x.strip()))
def test_partial_update_preserves_other_fields(new_name):
    db = _fresh_db()
    try:
        user = _make_candidate(db)
        service = CandidateService(db)
        original = service.create_profile(user.id, ProfileCreateSchema(
            name="Original",
            skills=["Python", "React"],
            education=["BS CS"],
            project_summaries=["Project A"],
            preferred_location="Remote",
        ))
        original_skills = list(original.skills)
        original_location = original.preferred_location

        # Update only the name
        updated = service.update_profile(user.id, ProfileUpdateSchema(name=new_name))

        assert updated.name == new_name
        assert updated.skills == original_skills  # unchanged
        assert updated.preferred_location == original_location  # unchanged
    finally:
        db.close()


# Property 5: Duplicate profile rejection
# Validates: Requirements 2.5

def test_duplicate_profile_rejected():
    db = _fresh_db()
    try:
        user = _make_candidate(db)
        service = CandidateService(db)
        data = ProfileCreateSchema(name="Jane", skills=["Python"], education=["BS"])
        service.create_profile(user.id, data)
        with pytest.raises(ConflictError):
            service.create_profile(user.id, data)
    finally:
        db.close()

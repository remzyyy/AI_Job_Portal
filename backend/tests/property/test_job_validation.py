"""Feature: ai-job-board — Property-based tests for job listing validation."""
import pytest
from hypothesis import given, strategies as st, settings, HealthCheck
from pydantic import ValidationError as PydanticValidationError

from app.schemas.job import JobCreateSchema, ExperienceLevel

VALID_LEVELS = ["Entry", "Mid", "Senior", "Lead"]


def _make_job(title, description, skills, level, location):
    return JobCreateSchema(
        title=title,
        description=description,
        required_skills=skills,
        experience_level=level,
        location=location,
    )


# Property 1: Job listing validation rejects invalid input with field-level errors
# Validates: Requirements 1.4, 1.5

@settings(max_examples=100)
@given(title=st.text(min_size=151, max_size=300))
def test_title_over_150_rejected(title):
    with pytest.raises(PydanticValidationError):
        _make_job(title, "desc", ["Python"], "Mid", "Remote")


@settings(max_examples=50)
@given(
    char=st.characters(min_codepoint=33, max_codepoint=126),
    extra=st.integers(min_value=1, max_value=200),
)
def test_description_over_5000_rejected(char, extra):
    # Build an over-length description from a repeated character to test the
    # boundary without generating large amounts of random entropy.
    description = char * (5000 + extra)
    with pytest.raises(PydanticValidationError):
        _make_job("Engineer", description, ["Python"], "Mid", "Remote")


@settings(max_examples=100)
@given(
    skills=st.lists(st.text(min_size=1, max_size=20), min_size=21, max_size=40, unique=True)
)
def test_more_than_20_skills_rejected(skills):
    with pytest.raises(PydanticValidationError):
        _make_job("Engineer", "desc", skills, "Mid", "Remote")


def test_zero_skills_rejected():
    with pytest.raises(PydanticValidationError):
        _make_job("Engineer", "desc", [], "Mid", "Remote")


def test_empty_title_rejected():
    with pytest.raises(PydanticValidationError):
        _make_job("", "desc", ["Python"], "Mid", "Remote")


def test_empty_location_rejected():
    with pytest.raises(PydanticValidationError):
        _make_job("Engineer", "desc", ["Python"], "Mid", "")


@settings(max_examples=100)
@given(level=st.text().filter(lambda x: x not in VALID_LEVELS))
def test_invalid_experience_level_rejected(level):
    with pytest.raises(PydanticValidationError):
        _make_job("Engineer", "desc", ["Python"], level, "Remote")


# Positive control: valid jobs are accepted
@settings(max_examples=100)
@given(
    title=st.text(min_size=1, max_size=150).filter(lambda x: x.strip()),
    description=st.text(min_size=1, max_size=5000).filter(lambda x: x.strip()),
    skills=st.lists(st.text(min_size=1, max_size=100).filter(lambda x: x.strip()),
                    min_size=1, max_size=20, unique=True),
    level=st.sampled_from(VALID_LEVELS),
    location=st.text(min_size=1, max_size=100).filter(lambda x: x.strip()),
)
def test_valid_job_accepted(title, description, skills, level, location):
    job = _make_job(title, description, skills, level, location)
    assert job.title == title
    assert len(job.required_skills) == len(skills)

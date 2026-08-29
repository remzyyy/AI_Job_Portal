"""Feature: ai-job-board — Integration tests for API endpoints via TestClient."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tests.conftest import auth_header


def test_health(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"


def test_create_job_returns_201(client, admin_user):
    res = client.post("/api/jobs", headers=auth_header(admin_user), json={
        "title": "Backend Engineer",
        "description": "Build APIs",
        "required_skills": ["Python", "FastAPI"],
        "experience_level": "Mid",
        "location": "Remote",
    })
    assert res.status_code == 201
    data = res.json()
    assert data["status"] == "open"
    assert data["title"] == "Backend Engineer"


def test_create_job_invalid_returns_400(client, admin_user):
    res = client.post("/api/jobs", headers=auth_header(admin_user), json={
        "title": "",  # empty
        "description": "desc",
        "required_skills": [],  # empty
        "experience_level": "Mid",
        "location": "Remote",
    })
    assert res.status_code == 400
    assert "details" in res.json() or "error" in res.json()


def test_get_nonexistent_job_returns_404(client):
    res = client.get("/api/jobs/9999")
    assert res.status_code == 404


def test_candidate_cannot_create_job(client, candidate_user):
    res = client.post("/api/jobs", headers=auth_header(candidate_user), json={
        "title": "Engineer",
        "description": "desc",
        "required_skills": ["Python"],
        "experience_level": "Mid",
        "location": "Remote",
    })
    assert res.status_code == 403


def test_full_apply_flow(client, admin_user, candidate_user):
    # Admin creates job
    job_res = client.post("/api/jobs", headers=auth_header(admin_user), json={
        "title": "Engineer",
        "description": "desc",
        "required_skills": ["Python"],
        "experience_level": "Mid",
        "location": "Remote",
    })
    job_id = job_res.json()["id"]

    # Candidate creates profile
    client.post("/api/candidates/profile", headers=auth_header(candidate_user), json={
        "name": "Jane",
        "skills": ["Python"],
        "education": ["BS CS"],
    })

    # Candidate applies
    apply_res = client.post(f"/api/jobs/{job_id}/apply", headers=auth_header(candidate_user))
    assert apply_res.status_code == 201
    assert apply_res.json()["status"] == "Applied"

    # Duplicate apply rejected (409)
    dup = client.post(f"/api/jobs/{job_id}/apply", headers=auth_header(candidate_user))
    assert dup.status_code == 409

    # Admin views applications
    apps = client.get(f"/api/jobs/{job_id}/applications", headers=auth_header(admin_user))
    assert apps.status_code == 200
    assert apps.json()["total"] == 1

    # Admin updates status
    app_id = apps.json()["items"][0]["id"]
    upd = client.patch(f"/api/applications/{app_id}/status",
                       headers=auth_header(admin_user), json={"status": "Shortlisted"})
    assert upd.status_code == 200
    assert upd.json()["status"] == "Shortlisted"


def test_apply_without_profile_returns_400(client, admin_user, candidate_user):
    job_res = client.post("/api/jobs", headers=auth_header(admin_user), json={
        "title": "Engineer", "description": "desc", "required_skills": ["Python"],
        "experience_level": "Mid", "location": "Remote",
    })
    job_id = job_res.json()["id"]
    res = client.post(f"/api/jobs/{job_id}/apply", headers=auth_header(candidate_user))
    assert res.status_code == 400


def test_ownership_enforced_on_applications(client, admin_user, second_admin, candidate_user):
    # admin_user creates job
    job_res = client.post("/api/jobs", headers=auth_header(admin_user), json={
        "title": "Engineer", "description": "desc", "required_skills": ["Python"],
        "experience_level": "Mid", "location": "Remote",
    })
    job_id = job_res.json()["id"]
    # second_admin tries to view applications -> 403
    res = client.get(f"/api/jobs/{job_id}/applications", headers=auth_header(second_admin))
    assert res.status_code == 403


def test_dashboard_zero_state(client, admin_user):
    res = client.get("/api/admin/dashboard", headers=auth_header(admin_user))
    assert res.status_code == 200
    data = res.json()
    assert data["status_breakdown"] == {"Applied": 0, "Shortlisted": 0, "Rejected": 0}
    assert data["applications_per_job"] == []

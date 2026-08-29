# Implementation Plan: AI Job Board

## Overview

This implementation plan builds the AI Job Board as a full-stack application with a Python FastAPI backend and React frontend. Tasks are ordered to establish foundations first (project structure, database models), then layer in backend services, API endpoints, frontend components, and finally integration and testing. Each task is scoped for incremental progress with no orphaned code.

## Tasks

- [ ] 1. Project setup and scaffolding
  - [ ] 1.1 Initialize backend project structure
    - Create `backend/` directory with `app/` subdirectories: `models/`, `schemas/`, `routers/`, `services/`, `utils/`
    - Create `backend/requirements.txt` with dependencies: fastapi, uvicorn, sqlalchemy, pydantic, openai, python-dotenv, pytest, hypothesis, httpx
    - Create `backend/app/__init__.py`, `backend/app/config.py` (Settings class using pydantic-settings with DATABASE_URL, OPENAI_API_KEY, PAGE_SIZE=20)
    - Create `backend/app/database.py` with SQLAlchemy engine, SessionLocal, Base, and get_db dependency
    - Create `backend/app/main.py` with FastAPI app instance, CORS middleware, exception handlers, and router includes
    - _Requirements: 8.1, 8.6, 10.1_

  - [ ] 1.2 Initialize frontend project structure
    - Create React project using Vite in `frontend/` directory
    - Set up `frontend/src/` with directories: `components/`, `pages/admin/`, `pages/candidate/`, `services/`, `hooks/`
    - Create `frontend/src/services/api.js` with base Axios/fetch configuration pointing to backend API
    - Create `frontend/src/hooks/useApi.js` custom hook for API calls with loading/error state management
    - Create `frontend/vite.config.js` with proxy to backend during development
    - _Requirements: 9.3, 10.1_

- [ ] 2. Database models and migrations
  - [ ] 2.1 Create SQLAlchemy ORM models
    - Create `backend/app/models/__init__.py` exporting all models
    - Create `backend/app/models/user.py` with User model (id, email unique, password_hash, role, created_at)
    - Create `backend/app/models/job_listing.py` with JobListing model (id, admin_id FK, title 150 chars, description text, required_skills JSON, experience_level, location, status default "open", created_at, updated_at)
    - Create `backend/app/models/candidate_profile.py` with CandidateProfile model (id, candidate_id FK unique, name, skills JSON, education JSON, project_summaries JSON, preferred_location, role_type, domain_interest, created_at, updated_at)
    - Create `backend/app/models/application.py` with Application model (id, candidate_id FK, job_id FK, status default "Applied", applied_at, updated_at, UniqueConstraint on candidate_id+job_id)
    - _Requirements: 1.1, 2.1, 4.1, 4.2_

  - [ ] 2.2 Create database initialization script
    - Add `create_all` call in `backend/app/database.py` or a separate `init_db.py` to create tables on startup
    - Add a seed script `backend/app/seed.py` that creates sample admin and candidate users for development
    - _Requirements: 10.3_

- [ ] 3. Pydantic schemas for request/response validation
  - [ ] 3.1 Create job listing schemas
    - Create `backend/app/schemas/job.py` with JobCreateSchema (title max 150, description max 5000, required_skills 1-20 items, experience_level enum, location non-empty), JobUpdateSchema (all optional), JobStatusUpdateSchema, JobResponseSchema, JobFilterSchema (skill, location, experience_level optional)
    - _Requirements: 1.1, 1.4, 1.5, 7.1, 7.2, 7.3_

  - [ ] 3.2 Create candidate and application schemas
    - Create `backend/app/schemas/candidate.py` with ProfileCreateSchema (name required, skills 1-50 items each ≤100 chars, education 1-20 entries, project_summaries 0-20, optional preferences ≤200 chars), ProfileUpdateSchema (all optional)
    - Create `backend/app/schemas/application.py` with ApplicationCreateSchema, ApplicationStatusUpdateSchema (enum: Applied, Shortlisted, Rejected), ApplicationResponseSchema
    - _Requirements: 2.1, 2.3, 2.4, 5.2, 5.3_

  - [ ] 3.3 Create matching and pagination schemas
    - Create `backend/app/schemas/matching.py` with MatchQuerySchema (query non-empty, max 1000 chars), MatchResultSchema (job_id, score 0-100, explanation), MatchResponseSchema
    - Create `backend/app/utils/pagination.py` with PaginatedResponse schema (items, total, page, total_pages) and paginate helper function
    - _Requirements: 3.1, 3.2, 3.4, 3.5, 8.7_

- [ ] 4. Backend utility layer
  - [ ] 4.1 Create custom exceptions and error handlers
    - Create `backend/app/utils/exceptions.py` with AppException, NotFoundError, AuthorizationError, ValidationError, ConflictError, ServiceUnavailableError
    - Register exception handlers in `main.py`: AppException handler returns structured JSON, generic handler returns 500 without internals, RequestValidationError handler transforms 422 to 400 with field-level details
    - _Requirements: 8.2, 8.3, 8.4, 8.5_

- [ ] 5. Backend services - Job and Candidate
  - [ ] 5.1 Implement JobService
    - Create `backend/app/services/job_service.py` with methods: create_job (validates admin role, creates with status "open"), update_job (validates ownership), update_status (validates ownership, validates status enum), get_job (raises NotFoundError), search_jobs (applies filters with AND logic, case-insensitive skill/location matching, only open listings, ordered by created_at desc, paginated)
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8_

  - [ ] 5.2 Implement CandidateService
    - Create `backend/app/services/candidate_service.py` with methods: create_profile (enforces one-per-candidate via ConflictError), update_profile (partial update preserving unmodified fields), get_profile (raises NotFoundError if missing)
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

- [ ] 6. Backend services - Application and Analytics
  - [ ] 6.1 Implement ApplicationService
    - Create `backend/app/services/application_service.py` with methods: apply (validates profile exists, validates job is open, validates no duplicate, creates with status "Applied"), get_applications_for_job (validates admin owns job, ordered by applied_at desc, paginated), update_status (validates admin owns the job, validates status enum), get_candidate_applications (paginated)
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 5.1, 5.2, 5.3, 5.4_

  - [ ] 6.2 Implement AnalyticsService
    - Create `backend/app/services/analytics_service.py` with methods: get_dashboard (aggregates all metrics), get_applications_per_job (count grouped by job for admin's listings), get_skills_distribution (count skills across applicants to admin's jobs), get_status_breakdown (count grouped by status for admin's listings). Return zero counts when no data exists.
    - _Requirements: 6.1, 6.2, 6.3, 6.4_

- [ ] 7. Backend services - AI Matching
  - [ ] 7.1 Implement MatchingService
    - Create `backend/app/services/matching_service.py` with methods: match (validates query non-empty and ≤1000 chars, rejects whitespace-only, fetches open jobs, builds prompt, calls OpenAI API, parses response, returns top 20 sorted by score desc), _build_prompt (formats candidate query + job summaries into structured prompt), _parse_response (parses JSON response into MatchResult list, handles malformed responses)
    - Handle OpenAI errors: timeout (30s), rate limiting (429), invalid response format, auth failure — all return 503 with retry guidance
    - Return empty result set with message when no matches found
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7_

- [ ] 8. Checkpoint - Backend services complete
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 9. API routers - Jobs and Candidates
  - [ ] 9.1 Implement jobs router
    - Create `backend/app/routers/jobs.py` with endpoints: POST /api/jobs (admin, 201), GET /api/jobs (any, paginated), GET /api/jobs/{id} (any), PUT /api/jobs/{id} (admin owner), PATCH /api/jobs/{id}/status (admin owner)
    - Wire to JobService, inject db session dependency, handle auth via request headers or simple role middleware
    - _Requirements: 1.1, 1.2, 1.3, 1.6, 1.7, 8.1, 8.2_

  - [ ] 9.2 Implement candidates router
    - Create `backend/app/routers/candidates.py` with endpoints: POST /api/candidates/profile (candidate, 201), GET /api/candidates/profile (candidate, own profile), PUT /api/candidates/profile (candidate)
    - Wire to CandidateService with session dependency
    - _Requirements: 2.1, 2.2, 2.5, 8.1, 8.2_

- [ ] 10. API routers - Applications, Matching, Analytics
  - [ ] 10.1 Implement applications router
    - Create `backend/app/routers/applications.py` with endpoints: POST /api/jobs/{id}/apply (candidate, 201), GET /api/jobs/{id}/applications (admin owner, paginated), PATCH /api/applications/{id}/status (admin), GET /api/candidates/applications (candidate, paginated)
    - Wire to ApplicationService
    - _Requirements: 4.1, 4.6, 5.1, 5.2, 5.4, 8.1, 8.2_

  - [ ] 10.2 Implement matching router
    - Create `backend/app/routers/matching.py` with endpoint: POST /api/matching (candidate)
    - Wire to MatchingService, return ranked results or appropriate error
    - _Requirements: 3.1, 3.4, 3.5, 3.7, 8.1_

  - [ ] 10.3 Implement analytics router
    - Create `backend/app/routers/analytics.py` with endpoint: GET /api/admin/dashboard (admin)
    - Wire to AnalyticsService, return aggregated metrics
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 8.1_

- [ ] 11. Checkpoint - Backend API complete
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 12. Frontend shared components
  - [ ] 12.1 Create shared UI components
    - Create `frontend/src/components/LoadingSpinner.jsx` — displays during API calls, used to disable submit buttons
    - Create `frontend/src/components/ErrorNotification.jsx` — shows API error messages, auto-dismisses after 5 seconds or manual dismiss
    - Create `frontend/src/components/Pagination.jsx` — page navigation controls for paginated lists (prev/next, page numbers)
    - Create `frontend/src/components/FormField.jsx` — input wrapper with label, inline validation message display
    - _Requirements: 9.4, 9.5, 9.6_

  - [ ] 12.2 Create App shell and routing
    - Create `frontend/src/App.jsx` with React Router setup: role-based route trees for `/admin/*` and `/candidate/*`
    - Add navigation header with role switching (simple toggle for demo purposes, no full auth)
    - Create basic layout wrapper component
    - _Requirements: 9.1, 9.2_

- [ ] 13. Frontend admin pages
  - [ ] 13.1 Implement Admin Dashboard page
    - Create `frontend/src/pages/admin/Dashboard.jsx` displaying: applications per job (bar chart or table), skill distribution, status breakdown (Applied/Shortlisted/Rejected counts)
    - Fetch data from GET /api/admin/dashboard on mount
    - Show zero counts gracefully when no data
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 9.1_

  - [ ] 13.2 Implement Job Manager page
    - Create `frontend/src/pages/admin/JobManager.jsx` with table of owned jobs showing title, status, created date
    - Add status toggle buttons (open/closed), edit and create navigation
    - Implement pagination for job list
    - _Requirements: 1.2, 1.3, 9.1_

  - [ ] 13.3 Implement Job Form page
    - Create `frontend/src/pages/admin/JobForm.jsx` — create/edit form with fields: title (≤150 chars), description (≤5000 chars), required skills (add/remove, 1-20), experience level (dropdown: Entry/Mid/Senior/Lead), location
    - Client-side validation before submit, inline error messages via FormField
    - POST for create, PUT for edit
    - _Requirements: 1.1, 1.4, 1.5, 9.5, 9.6_

  - [ ] 13.4 Implement Application Review page
    - Create `frontend/src/pages/admin/ApplicationReview.jsx` — list applications for a selected job
    - Display candidate name, skills, applied date, current status
    - Add status update dropdown (Applied/Shortlisted/Rejected) per application
    - _Requirements: 5.1, 5.2, 5.3, 9.1_

- [ ] 14. Frontend candidate pages
  - [ ] 14.1 Implement Candidate Profile page
    - Create `frontend/src/pages/candidate/Profile.jsx` — form for creating/editing profile
    - Fields: name, skills (multi-input, 1-50), education (multi-input, 1-20), project summaries (multi-input, 0-20), preferred location, role type, domain interest (all optional, ≤200 chars)
    - Client-side validation, shows existing profile for editing if one exists
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 9.2, 9.5_

  - [ ] 14.2 Implement Job Search page
    - Create `frontend/src/pages/candidate/JobSearch.jsx` — filterable job listing view
    - Filter inputs: skill, location, experience level
    - Results displayed as cards/list with title, location, experience level, skills
    - Pagination for results, click-through to job detail
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 9.2_

  - [ ] 14.3 Implement AI Matching page
    - Create `frontend/src/pages/candidate/AIMatching.jsx` — natural language input textarea (≤1000 chars)
    - Submit to POST /api/matching, display ranked results with score badge and explanation text
    - Handle loading state, empty results with message, and service unavailable errors
    - _Requirements: 3.1, 3.2, 3.4, 3.5, 3.6, 3.7, 9.2, 9.6_

  - [ ] 14.4 Implement My Applications page
    - Create `frontend/src/pages/candidate/MyApplications.jsx` — list of submitted applications
    - Display job title, application status, applied date
    - Paginated view
    - _Requirements: 4.6, 9.2_

- [ ] 15. Checkpoint - Frontend complete
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 16. Integration, testing, and documentation
  - [ ]* 16.1 Write property-based tests for job validation
    - **Property 1: Job listing validation rejects invalid input with field-level errors**
    - **Validates: Requirements 1.4, 1.5**
    - Create `backend/tests/property/test_job_validation.py` using Hypothesis
    - Strategy: generate invalid job inputs (empty title, title >150, empty description, description >5000, 0 or >20 skills, invalid experience level, empty location) and verify rejection with field-level errors

  - [ ]* 16.2 Write property-based tests for profile management
    - **Property 3: Profile partial update preserves unmodified fields**
    - **Property 4: Candidate profile validation rejects missing required fields**
    - **Property 5: Duplicate profile rejection**
    - **Validates: Requirements 2.2, 2.4, 2.5**
    - Create `backend/tests/property/test_profile_management.py` using Hypothesis

  - [ ]* 16.3 Write property-based tests for application rules
    - **Property 9: Applications to closed listings are rejected**
    - **Property 10: Duplicate applications are rejected**
    - **Property 11: Applications require a candidate profile**
    - **Validates: Requirements 4.3, 4.4, 4.5**
    - Create `backend/tests/property/test_application_rules.py` using Hypothesis

  - [ ]* 16.4 Write property-based tests for AI matching structure
    - **Property 6: AI match results are bounded, scored, ordered, and explained**
    - **Property 7: AI matching only returns open listings**
    - **Property 8: Whitespace-only queries are rejected**
    - **Validates: Requirements 3.1, 3.2, 3.3, 3.4**
    - Create `backend/tests/property/test_matching_structure.py` using Hypothesis with mocked OpenAI responses

  - [ ]* 16.5 Write property-based tests for search and pagination
    - **Property 14: Search filters use AND logic with case-insensitive matching**
    - **Property 15: Search results only include open listings**
    - **Property 16: Search results are ordered by creation date descending**
    - **Property 17: Pagination structure for large result sets**
    - **Validates: Requirements 7.1, 7.2, 7.3, 7.4, 7.5, 7.8, 8.7**
    - Create `backend/tests/property/test_search_filters.py` and `test_pagination.py` using Hypothesis

  - [ ]* 16.6 Write property-based tests for ownership and analytics
    - **Property 2: Job listing ownership authorization**
    - **Property 12: Application management respects job ownership**
    - **Property 13: Dashboard metrics accurately reflect underlying data**
    - **Property 18: Validation errors identify failing fields**
    - **Validates: Requirements 1.7, 5.4, 6.1, 6.2, 6.3, 8.3**
    - Create `backend/tests/property/test_ownership.py` and `test_analytics.py` using Hypothesis

  - [ ]* 16.7 Write unit tests for backend services
    - Create `backend/tests/unit/test_job_service.py` — happy path CRUD, boundary values (150 char title, 20 skills)
    - Create `backend/tests/unit/test_candidate_service.py` — profile creation, partial updates
    - Create `backend/tests/unit/test_application_service.py` — apply flow, status transitions
    - Create `backend/tests/unit/test_matching_service.py` — prompt construction, response parsing, error handling
    - Create `backend/tests/unit/test_analytics_service.py` — metric accuracy, zero data scenarios
    - _Requirements: 1.1–1.8, 2.1–2.5, 3.1–3.7, 4.1–4.6, 5.1–5.4, 6.1–6.4_

  - [ ]* 16.8 Write integration tests for API endpoints
    - Create `backend/tests/integration/test_api_endpoints.py` using FastAPI TestClient
    - Test full request/response cycles for all endpoints
    - Verify correct HTTP status codes (201 for creation, 200 for retrieval/update, 400/403/404/409/503 for errors)
    - Create `backend/tests/conftest.py` with test database setup, fixtures for admin/candidate users
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

  - [ ] 16.9 Create project README
    - Create `README.md` at project root with sections: Tech Stack (FastAPI, SQLAlchemy, React, Vite, OpenAI API), Architecture Decisions (client-server separation, SQLite for simplicity, role-based routing), Setup Instructions (backend: pip install, uvicorn run; frontend: npm install, npm run dev), Environment Variables (OPENAI_API_KEY), Assumptions
    - _Requirements: 10.2, 10.3_

- [ ] 17. Final checkpoint - All integration complete
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties from the design document
- Unit tests validate specific examples and edge cases
- The backend uses Python with FastAPI; the frontend uses React with JavaScript (JSX)
- OpenAI API integration requires an API key set via environment variable
- SQLite is used for development; the ORM layer supports migration to PostgreSQL later

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "1.2"] },
    { "id": 1, "tasks": ["2.1", "2.2"] },
    { "id": 2, "tasks": ["3.1", "3.2", "3.3"] },
    { "id": 3, "tasks": ["4.1"] },
    { "id": 4, "tasks": ["5.1", "5.2"] },
    { "id": 5, "tasks": ["6.1", "6.2", "7.1"] },
    { "id": 6, "tasks": ["9.1", "9.2"] },
    { "id": 7, "tasks": ["10.1", "10.2", "10.3"] },
    { "id": 8, "tasks": ["12.1", "12.2"] },
    { "id": 9, "tasks": ["13.1", "13.2", "13.3", "13.4"] },
    { "id": 10, "tasks": ["14.1", "14.2", "14.3", "14.4"] },
    { "id": 11, "tasks": ["16.1", "16.2", "16.3", "16.4", "16.5", "16.6"] },
    { "id": 12, "tasks": ["16.7", "16.8"] },
    { "id": 13, "tasks": ["16.9"] }
  ]
}
```

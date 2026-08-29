# AI Job Board

A full-stack job board web application with AI-powered candidate matching. Company Admins post and manage job listings; Candidates create profiles, browse jobs, and apply. Candidates can also describe their ideal role in natural language and receive AI-ranked job matches with explanations.

## Tech Stack

**Backend**
- Python 3.10+
- FastAPI (RESTful API framework)
- SQLAlchemy 2.0 (ORM)
- SQLite (database — zero-config, file-based)
- OpenAI API (natural language job matching, with a keyword-based fallback)
- JWT auth (python-jose) + bcrypt password hashing (passlib)

**Frontend**
- React 18
- Vite (dev server + build tool)
- React Router (role-based routing)
- Axios (API client)

## Architecture Decisions

- **Client–server separation**: The backend is a stateless JSON API under `/api`; the React frontend consumes it. This keeps concerns cleanly separated and allows independent scaling/deployment.
- **Service layer pattern**: Business logic lives in `services/` (JobService, CandidateService, ApplicationService, MatchingService, AnalyticsService), keeping routers thin and logic testable.
- **SQLite for simplicity**: Chosen for zero-config local development. The SQLAlchemy ORM layer provides a clean upgrade path to PostgreSQL by changing only `DATABASE_URL`.
- **AI matching with graceful fallback**: When an `OPENAI_API_KEY` is configured, the matching engine uses GPT to score and explain matches. Without a key (or on API failure), it falls back to a transparent keyword-scoring algorithm so the feature always works during a demo.
- **Role-based routing**: The frontend renders separate route trees for `admin/*` and `candidate/*`, guarded by the authenticated user's role.

## Project Structure

```
Project_aami/
├── backend/          # FastAPI application
│   ├── app/
│   │   ├── models/       # SQLAlchemy ORM models
│   │   ├── schemas/      # Pydantic request/response schemas
│   │   ├── routers/      # API route handlers
│   │   ├── services/     # Business logic
│   │   ├── utils/        # Auth, exceptions, pagination
│   │   ├── main.py       # App entry point
│   │   ├── config.py     # Settings
│   │   ├── database.py   # DB engine/session
│   │   └── seed.py       # Sample data seeder
│   └── requirements.txt
├── frontend/         # React application
│   ├── src/
│   │   ├── components/   # Shared UI components
│   │   ├── pages/        # admin/ and candidate/ views
│   │   ├── services/     # API client
│   │   ├── hooks/        # useApi hook
│   │   └── context/      # Auth context
│   └── package.json
└── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+
### Find Path(Backend Fronted)

```bash
pwd
dir

cd Project_aami
dir

# After dir you can write command-

# For backend -
cd backend
uvicorn app.main:app --reload --port 8000

# For Frontend-
cd frontend
npm run dev





```
### Backend

```bash
cd backend
pip install -r requirements.txt

# (optional) add your OpenAI key for real AI matching
# edit backend/.env and set OPENAI_API_KEY=sk-...

# seed the database with sample users and jobs
python -m app.seed

# start the API server
uvicorn app.main:app --reload --port 8000
```

The API runs at `http://localhost:8000`. Interactive docs: `http://localhost:8000/docs`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The app runs at `http://localhost:5173` and proxies `/api` calls to the backend.

## Demo Accounts

After seeding, log in with:

| Role      | Email                   | Password      |
|-----------|-------------------------|---------------|
| Admin     | admin@example.com       | admin123      |
| Candidate | candidate@example.com   | candidate123  |

## Features

- **Company Admin**: create/edit/manage job listings, open/close listings, review applications, update pipeline status (Applied → Shortlisted → Rejected), analytics dashboard.
- **Candidate**: create/edit profile, search & filter jobs, AI natural-language matching, apply to jobs, track application status.
- **AI Matching**: type a description like "Python backend role in a healthcare startup" and get ranked matches with explanations.

## Assumptions

- Authentication is JWT-based with a simple email/password scheme sufficient for the assignment; it is not hardened for production (the secret key is a dev default).
- One candidate profile per candidate account.
- A candidate cannot apply to the same job twice, and cannot apply to closed listings.
- The AI matching falls back to keyword scoring when no OpenAI key is present, so the feature is fully demonstrable offline.
- SQLite is used for the demo; the schema is Postgres-compatible via SQLAlchemy.
- Admins only see and manage their own job listings and the applications to them.

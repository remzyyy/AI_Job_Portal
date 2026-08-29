# AI Job Board — Demo Presentation

> Speaker notes + slide content for the live 30-minute Teams demo.
> 4 slides. Present in your own words; the bullets are prompts, not a script to read.

---

## Slide 1 — Objective

### AI Job Board with AI-Powered Candidate Matching

**The problem it solves**
- Company Admins post and manage job listings
- Candidates create profiles, browse jobs, and apply
- The differentiator: candidates describe their ideal role in **plain English**, and the system **ranks matching jobs and explains why** each one fits

**Two roles, one platform**
- **Company Admin** → create/manage jobs, review applications, track a hiring pipeline, view analytics
- **Candidate** → build a profile, search/filter jobs, get AI matches, apply, track status

**Tech stack (3 days, full-stack + AI)**
- Backend: **Python + FastAPI**, SQLAlchemy, SQLite
- Frontend: **React + Vite**
- AI: **OpenAI GPT** for semantic matching, with a keyword fallback so it always works

*Speaker note: Lead with the AI matching — it's the centerpiece and what makes this more than a CRUD app.*

---

## Slide 2 — System Architecture

```
┌───────────────────────────┐        ┌──────────────────────────────────┐
│      FRONTEND (React)      │        │        BACKEND (FastAPI)          │
│                            │  HTTP  │                                    │
│  Admin views               │ ─JSON→ │  Routers (REST endpoints)          │
│   • Dashboard              │        │      ↓                             │
│   • Job Manager / Form     │        │  Services (business logic)         │
│   • Application Review     │        │   • JobService                     │
│                            │        │   • CandidateService               │
│  Candidate views           │ ←JSON─ │   • ApplicationService             │
│   • Profile                │        │   • MatchingService ──► OpenAI API │
│   • Job Search             │        │   • AnalyticsService               │
│   • AI Matching            │        │      ↓                             │
│   • My Applications        │        │  SQLAlchemy ORM ──► SQLite DB       │
└───────────────────────────┘        └──────────────────────────────────┘
```

**Design principles**
- **Clean client–server split** — stateless JSON API under `/api`, React consumes it
- **Layered backend** — Routers (thin) → Services (logic) → ORM (data). Keeps logic testable and swappable.
- **Auth** — JWT tokens, role-based access (admin vs candidate) enforced on every protected route
- **Data model** — Users, JobListings, CandidateProfiles, Applications (one profile per candidate; one application per candidate-job pair)

*Speaker note: Point at the MatchingService → OpenAI arrow — that's the AI integration boundary.*

---

## Slide 3 — End-to-End Workflow

```
ADMIN                              CANDIDATE
  │                                   │
  ├─ Create job listing               ├─ Create profile (skills, education, prefs)
  │  (title, skills, level,           │
  │   location, open/closed)          ├─ Option A: Search & filter
  │                                   │    by skill / location / level
  │                                   │
  │                                   ├─ Option B: AI Matching ★
  │                                   │    "Python backend role in a
  │                                   │     healthcare startup, remote"
  │                                   │         ↓
  │                                   │    Ranked jobs + match scores
  │                                   │    + explanation for each
  │                                   │
  │                                   ├─ Apply to a job
  │                                   │    (profile-required, no
  │                                   │     duplicates, no closed jobs)
  │                                   │
  ├─ Review applications  ◄───────────┘
  ├─ Update status:
  │    Applied → Shortlisted → Rejected
  │
  └─ Dashboard analytics
       • applications per job
       • skill distribution
       • pipeline status counts
```

**How the AI matching works (the ★ step)**
1. Validate the query (non-empty, ≤1000 chars)
2. Fetch all **open** job listings
3. Build a structured prompt (query + job summaries) → send to GPT
4. Parse JSON response → scores (0–100) + explanations
5. Rank by score, return top 20
6. *Fallback:* if no API key / API fails → transparent keyword scoring

*Speaker note: Demo this live — type a natural-language query and show the ranked, explained results.*

---

## Slide 4 — Engineering Quality & What I'd Improve

**What's solid**
- **Validation & error handling** — proper HTTP codes (200/201/400/403/404/409/500), field-level error messages, no internal details leaked on 500s
- **Business rules enforced** — ownership checks, duplicate prevention, closed-job blocking, one-profile-per-candidate
- **Tested** — 34 automated tests: property-based (Hypothesis) for universal invariants + integration tests (FastAPI TestClient) for endpoints
- **Resilient AI** — graceful fallback means the feature never dies in a demo

**Honest limitations (be ready to discuss)**
- Auth is JWT but not production-hardened (dev secret key, no refresh tokens)
- SQLite for simplicity — ORM makes Postgres a config change away
- AI matching sends job summaries per request (no caching / embeddings yet)
- No pagination cursors — offset-based, fine at this scale

**What I'd do next**
- Vector embeddings + semantic search to reduce LLM cost and improve recall
- Rate limiting + caching on the matching endpoint
- Refresh tokens, password reset, email verification
- Frontend component tests (Vitest + React Testing Library)

*Speaker note: The brief rewards honesty — "what works, what doesn't, how I'd fix it." Lean into this slide.*

---

## Quick demo runbook (for your own reference)

1. **Both servers running?** Backend `uvicorn app.main:app --port 8000`, Frontend `npm run dev`
2. Open `http://localhost:5173`
3. **Log in as Candidate** (`candidate@example.com` / `candidate123`)
   - Show Job Search with filters (skill / Indian location / level)
   - Show **AI Matching** — type a natural-language query, show ranked results + explanations
   - Apply to a job
4. **Log in as Admin** (`admin@example.com` / `admin123`)
   - Show Job Manager → create a job live
   - Show Application Review → move a candidate Applied → Shortlisted
   - Show Dashboard → analytics update
5. Mention: 24 seeded jobs across Indian + global locations, 34 passing tests
```

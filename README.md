# VeriVote — Customizable Web-Based Electronic Voting System

VeriVote is a multi-tenant, customizable electronic voting platform built with **FastAPI**, **SQLAlchemy 2.0**, **PostgreSQL / SQLite**, **Jinja2 Templates**, and **Tailwind CSS + Vanilla JS**. It unifies **Single-Choice**, **Multiple-Choice (bounded min/max)**, and **Ranked-Choice Voting (Instant-Runoff)** inside a single configurable election engine while enforcing strict email + OTP accreditation and 3NF decoupled ballot secrecy.

---

## Table of Contents
1. [Architecture & Security Invariant](#architecture--security-invariant)
2. [Database Schema (8 Normalized 3NF Tables)](#database-schema-8-normalized-3nf-tables)
3. [Repository Structure](#repository-structure)
4. [Local Setup Guide (Windows & macOS/Linux)](#local-setup-guide-windows--macoslinux)
5. [Running the App & Tests](#running-the-app--tests)
6. [Git Branching & Team Contribution Workflow](#git-branching--team-contribution-workflow)
7. [Sprint Roadmap](#sprint-roadmap)

---

## Architecture & Security Invariant

- **Three-Tier Architecture**:
  1. **Presentation Tier (`frontend/`)**: HTML5, Tailwind CSS, Jinja2 Templates, and Vanilla JS (`fetch()`).
  2. **FastAPI ASGI Tier (`app/`)**: Uvicorn / FastAPI CLI server, versioned REST routers (`/api/v1`), Pydantic v2 validation, SQLAlchemy 2.0 ORM, and three lean services (`AuthService`, `VotingService`, `TabulationService`).
  3. **Data & Services Tier**: PostgreSQL (Neon in production / Docker locally) or SQLite (zero-setup local dev) + SMTP OTP dispatch.
- **3NF Anonymity Air-Gap**: `voter_eligibility` tracks accreditation and `voted_at`, while `anonymous_ballots` and `ballot_choices` store cast selections with **zero foreign keys** to `voter_eligibility`, **zero timestamps**, and random `UUIDv4` primary keys.

---

## Database Schema (8 Normalized 3NF Tables)

| # | Table | Purpose |
|---|---|---|
| 1 | `users` | Super-Admin and Election Organizer accounts (`role`, `is_active`) |
| 2 | `elections` | Timestamp-driven lifecycle (`DRAFT`, `UPCOMING`, `ACTIVE`, `CLOSED`, `CANCELLED` derived from `published_at`, `cancelled_at`, `start_time`, `end_time`) |
| 3 | `voter_eligibility` | Accredited email roster, optional `voter_ref`, expiring hashed OTPs, and `voted_at` |
| 4 | `ballot_questions` | Questions with `rule_type` (`SINGLE` \| `MULTI` \| `RANKED`), `is_required`, `min_select`, `max_select` |
| 5 | `candidate_options` | Candidate or motion choices per ballot question |
| 6 | `anonymous_ballots` | Secret ballot paper (`receipt_hash` unique, zero `voter_id`, zero timestamps) |
| 7 | `ballot_choices` | Individual selections or `rank_position` rows linked to `anonymous_ballots` |
| 8 | `audit_logs` | Immutable governance and security log (`JSONB` on PostgreSQL, `JSON` on SQLite) |

---

## Repository Structure

```text
VeriVote/
├── .github/workflows/ci.yml   # GitHub Actions CI (ruff + pytest on dev & main)
├── .env.example               # Environment variable template (copy to .env)
├── alembic/                   # Database migrations
├── app/
│   ├── main.py                # FastAPI app factory, CORS, Jinja2 & static mount
│   ├── core/config.py         # Pydantic Settings (.env loader)
│   ├── db/                    # SQLAlchemy Base, engine (with Neon pool_recycle), get_db()
│   ├── models/                # 8 SQLAlchemy 2.0 ORM models + enums
│   ├── schemas/               # Pydantic request/response schemas
│   ├── services/              # AuthService, VotingService, TabulationService
│   └── api/v1/                # Versioned REST endpoints (/api/v1/health, ...)
├── frontend/                  # Jinja2 HTML templates, CSS, and Vanilla JS
├── tests/                     # Pytest suite (isolated in-memory SQLite)
├── docker-compose.yml         # Optional local PostgreSQL 16 container
└── pyproject.toml             # Single source of truth for dependencies, ruff, & pytest
```

---

## Local Setup Guide (Windows & macOS/Linux)

> **Prerequisites:** Python **3.12+** and Git installed.

### 1. Clone the Repository
By default, cloning puts you on the **`dev`** branch (our active integration branch).

```bash
git clone https://github.com/DonaldXoftDev/VeriVote.git
cd VeriVote
```

### 2. Create a Virtual Environment & Install Dependencies
All dependencies are defined in `pyproject.toml` (there is no `requirements.txt`).

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```
*(If PowerShell blocks `Activate.ps1`, either run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` once, or skip activation and use `.\.venv\Scripts\pip install -e ".[dev]"`.)*

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### 3. Configure `.env`
`.env` is git-ignored so secrets are never pushed to GitHub. Create yours from `.env.example`:

**Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
```

**macOS / Linux:**
```bash
cp .env.example .env
```

By default, `.env.example` uses **SQLite** (`sqlite:///./verivote.db`) so you can start coding immediately without installing PostgreSQL.
- To use **Neon PostgreSQL** or local Docker PostgreSQL (`docker compose up -d`), replace `DATABASE_URL` in `.env` with your PostgreSQL connection string (`postgresql://...`).

### 4. Run Database Migrations
```bash
alembic upgrade head
```

---

## Running the App & Tests

### Start the Local Server
```bash
uvicorn app.main:app --reload
```
- **Landing Page:** `http://localhost:8000/`
- **Interactive Swagger API Docs:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`
- **Health Check:** `http://localhost:8000/api/v1/health`

### Run Linter & Tests Before Pushing
Every Pull Request must pass both **Ruff** and **Pytest**:
```bash
ruff check .
pytest
```

---

## Git Branching & Team Contribution Workflow

VeriVote uses a two-tier branch model:
- **`dev` (Default Branch):** Active sprint integration branch where team features are merged and tested together.
- **`main` (Production Branch):** Stable release branch deployed to FastAPI Cloud. Completed sprints are merged from `dev` -> `main`.

### How to Contribute a Feature
1. **Sync `dev` before starting:**
   ```bash
   git checkout dev
   git pull origin dev
   ```
2. **Create a feature branch off `dev`:**
   ```bash
   git checkout -b feat/your-feature-name
   ```
   *(Examples: `feat/sprint1-auth-service`, `ui/voter-booth`, `fix/otp-expiry`)*
3. **Make your changes, lint, and test:**
   ```bash
   ruff check .
   pytest
   ```
4. **Commit and push your feature branch (never push directly to `main`):**
   ```bash
   git add .
   git commit -m "feat: short description of your change"
   git push -u origin feat/your-feature-name
   ```
5. **Open a Pull Request on GitHub** targeting **`dev`**, wait for the `lint-and-test` check to turn green, and merge.

See [CONTRIBUTING.md](CONTRIBUTING.md) for architectural rules (including the ballot secrecy air-gap and the 4-Question Model-vs-Service Rubric).

---

## Sprint Roadmap

- **Sprint 0 (Complete):** FastAPI + SQLAlchemy 3NF 8-table schema, Alembic migration setup, 3 lean service stubs (`AuthService`, `VotingService`, `TabulationService`), Jinja2/Tailwind/Vanilla JS starter UI, GitHub Actions CI, Neon DB + FastAPI Cloud deployment, and unit/smoke tests.
- **Sprint 1:** `AuthService` (organizer signup, Super-Admin activation, login), draft election builder, CSV email-roster import, and SMTP OTP verification.
- **Sprint 2:** Dynamic ballot rendering (`SINGLE`, `MULTI`, `RANKED`), one-shot ballot submission, and atomic `SELECT ... FOR UPDATE` transaction.
- **Sprint 3:** `TabulationService` (Direct Count + Instant-Runoff elimination), timestamp-driven result unsealing, and `receipt_hash` verification.
- **Sprint 4:** Live turnout analytics, `audit_logs` viewer, `pytest` suite expansion, and final report/defense preparation.

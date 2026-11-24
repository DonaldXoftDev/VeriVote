# VeriVote — Customizable Web-Based Electronic Voting System

VeriVote is a multi-tenant, customizable electronic voting platform built with **FastAPI**, **SQLAlchemy 2.0**, **PostgreSQL / SQLite**, **Jinja2 Templates**, and **Tailwind CSS + Vanilla JS**. It unifies **Single-Choice**, **Multiple-Choice (bounded min/max)**, and **Ranked-Choice Voting (Instant-Runoff)** inside a single configurable election engine while enforcing strict email+OTP accreditation and 3NF decoupled ballot secrecy.

---

## Core Architecture & Security Invariant

- **Three-Tier Architecture**:
  1. **Presentation Tier (`frontend/`)**: HTML5, Tailwind CSS, Jinja2 Templates, and Vanilla JS (`fetch()`).
  2. **FastAPI ASGI Tier (`app/`)**: Uvicorn ASGI server, versioned REST routers (`/api/v1`), Pydantic validation, SQLAlchemy ORM, and three lean services (`AuthService`, `VotingService`, `TabulationService`).
  3. **Data & Services Tier**: PostgreSQL (production) / SQLite (local dev) + SMTP OTP dispatch.
- **3NF Anonymity Air-Gap**: `voter_eligibility` tracks accreditation and `voted_at`, while `anonymous_ballots` and `ballot_choices` store cast selections with **zero foreign keys** to `voter_eligibility`, **zero timestamps**, and random `UUIDv4` primary keys.

### 8 Normalized (3NF) Database Tables
1. `users` — Super-Admin and Election Organizer accounts (`role`, `is_active`)
2. `elections` — Timestamp-driven lifecycle container (`DRAFT`, `UPCOMING`, `ACTIVE`, `CLOSED`, `CANCELLED` derived from `published_at`, `cancelled_at`, `start_time`, `end_time`)
3. `voter_eligibility` — Accredited email roster, optional `voter_ref`, expiring hashed OTPs, and `voted_at`
4. `ballot_questions` — Questions with `rule_type` (`SINGLE` | `MULTI` | `RANKED`), `is_required`, `min_select`, `max_select`
5. `candidate_options` — Choices per ballot question
6. `anonymous_ballots` — Secret ballot paper (`receipt_hash` unique, zero `voter_id`, zero timestamps)
7. `ballot_choices` — Individual selections or `rank_position` rows linked to `anonymous_ballots`
8. `audit_logs` — Immutable governance and security log (`JSONB` metadata)

---

## Quick Start (Local Development)

### 1. Create a Virtual Environment & Install Dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### 2. Configure Environment
```bash
cp .env.example .env
```

### 3. Run Database Migrations
```bash
alembic upgrade head
```

### 4. Start the Development Server
```bash
uvicorn app.main:app --reload
```
- Frontend UI: `http://localhost:8000/`
- Interactive API Docs (Swagger): `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/api/v1/health`

### 5. Run Tests & Linter
```bash
ruff check .
pytest
```

---

## Sprint Roadmap

- **Sprint 0 (Current)**: FastAPI + SQLAlchemy 3NF 8-table schema, Alembic migration setup, 3 lean service stubs (`AuthService`, `VotingService`, `TabulationService`), Jinja2/Tailwind/Vanilla JS starter UI, CI workflow, and unit/smoke tests.
- **Sprint 1**: `AuthService` (organizer signup, Super-Admin activation, login), draft election builder, CSV email-roster import, and SMTP OTP verification.
- **Sprint 2**: Dynamic ballot rendering (`SINGLE`, `MULTI`, `RANKED`), one-shot ballot submission, and atomic `SELECT ... FOR UPDATE` transaction.
- **Sprint 3**: `TabulationService` (Direct Count + Instant-Runoff elimination), timestamp-driven result unsealing, and `receipt_hash` verification.
- **Sprint 4**: Live turnout analytics, `audit_logs` viewer, `pytest` suite expansion, and final report/defense preparation.

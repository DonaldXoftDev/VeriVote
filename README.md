# VeriVote — Customizable Web-Based Electronic Voting System

VeriVote is a multi-tenant, customizable electronic voting platform built with **FastAPI**, **SQLAlchemy 2.0**, **PostgreSQL / SQLite**, and **HTML5 + Tailwind CSS + Vanilla JS**. It unifies **Single-Choice**, **Multiple-Choice (bounded min/max)**, and **Ranked-Choice Voting (Instant-Runoff)** inside a single configurable election engine while enforcing strict voter accreditation and decoupled ballot secrecy.

---

## Core Architecture & Security Invariant

- **Three-Tier Architecture**:
  1. **Presentation Tier (`frontend/`)**: Responsive HTML5, Tailwind CSS, Vanilla CSS, and Vanilla JS (`fetch()`).
  2. **FastAPI ASGI Tier (`app/`)**: Uvicorn ASGI server, versioned REST routers (`/api/v1`), Pydantic validation, SQLAlchemy ORM, and `TabulationAndVotingEngine`.
  3. **Data & Services Tier**: PostgreSQL (production) / SQLite (local dev) + SMTP/OTP dispatch.
- **Anonymity Air-Gap**: `voter_eligibility` tracks accreditation and `has_voted`, while `anonymous_votes` stores cast selections. There is **no foreign key** or direct link between them.

### Core Database Tables (Section 7.2)
1. `organizers` — Election administrator accounts
2. `elections` — Election container (`auth_mode`, `status`, `start_time`, `end_time`)
3. `voter_eligibility` — Accredited voter hashes, single-use OTP/voucher hashes, `has_voted`
4. `ballot_questions` — Questions with `rule_type` (`SINGLE` | `MULTI` | `RANKED`) and `min_select` / `max_select`
5. `candidate_options` — Choices per ballot question
6. `anonymous_votes` — Secret ballot box with `receipt_hash` and optional `rank_position`

---

## Quick Start (Local Development)

### 1. Create a Virtual Environment & Install Dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
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

- **Sprint 0 (Current)**: Project scaffold, FastAPI app factory, 6-table SQLAlchemy domain schema, Alembic migration setup, CI workflow, Tailwind/Vanilla JS starter UI, and smoke tests.
- **Sprint 1**: Organizer registration/login, election CRUD & lifecycle states (`DRAFT`, `UPCOMING`, `ACTIVE`, `CLOSED`, `CANCELLED`), CSV roster import, and OTP/voucher accreditation.
- **Sprint 2**: Dynamic ballot builder, client & server rule validation, and atomic two-table vote submission (`SELECT ... FOR UPDATE`).
- **Sprint 3**: Multi-algorithm tabulation engine (Plurality, Multi-Choice, and Instant-Runoff RCV), sealed result disclosure, and receipt-hash verification.
- **Sprint 4**: Live turnout analytics, round-by-round runoff breakdown UI, and exportable audit reports.

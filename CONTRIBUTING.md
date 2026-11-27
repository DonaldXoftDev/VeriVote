# Contributing to VeriVote

## Branch Model
- **`main` (Default / Production Branch):** Stable release branch deployed to FastAPI Cloud. Completed sprints are merged from `dev` -> `main`.
- **`dev` (Integration Branch):** Active sprint integration branch. Always switch to `dev` (`git checkout dev`) after cloning, and target all feature PRs into `dev`.

Both `dev` and `main` are protected by `TeamCollab Ruleset` (Pull Request + passing `lint-and-test` CI check required).

## Feature Branch & Pull Request Workflow
1. Sync `dev` before starting a task:
   ```bash
   git checkout dev
   git pull origin dev
   ```
2. Create a descriptive feature branch off `dev`:
   ```bash
   git checkout -b feat/sprint1-auth-service
   ```
   *(Examples: `feat/sprint1-auth-service`, `ui/voter-booth`, `fix/otp-expiry`)*
3. Commit small, focused changes with clear messages.
4. Run linting and tests before pushing:
   ```bash
   ruff check .
   pytest
   ```
5. Push your branch and open a Pull Request against **`dev`**:
   ```bash
   git push -u origin feat/sprint1-auth-service
   ```
6. Wait for the **`lint-and-test`** check to turn green, then merge into `dev`.

## Architectural Rules
- **Ballot Secrecy Air-Gap:** Never add a `voter_id`, foreign key, or timestamp to `anonymous_ballots` or `ballot_choices`.
- **4-Question Model-vs-Service Rubric:** Keep database queries, external I/O (Bcrypt, SMTP, CSV), and multi-table transactions in `AuthService`, `VotingService`, and `TabulationService`; keep pure single-object checks (`get_state()`, `is_open()`, `is_editable()`, `has_voted()`, `validate_choices()`) on the ORM models.
- **Atomic One-Shot Submission:** Vote submission must lock `voter_eligibility` (`SELECT ... FOR UPDATE`), verify `voted_at IS NULL`, insert 1 `AnonymousBallot` + *N* `BallotChoice` rows, and set `voted_at = NOW()` in one transaction.

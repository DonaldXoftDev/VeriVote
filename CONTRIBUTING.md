# Contributing to VeriVote

## Branching & Pull Request Workflow
1. Always pull the latest `dev` before starting a task:
   ```bash
   git checkout dev && git pull origin dev
   ```
2. Create a descriptive feature branch:
   ```bash
   git checkout -b feat/sprint1-auth-service
   ```
3. Commit small, focused changes with clear messages.
4. Run linting and tests before pushing:
   ```bash
   ruff check .
   pytest
   ```
5. Push your branch and open a Pull Request against `dev`:
   ```bash
   git push -u origin feat/sprint1-auth-service
   ```

## Architectural Rules
- **Ballot Secrecy Air-Gap**: Never add a `voter_id`, foreign key, or timestamp to `anonymous_ballots` or `ballot_choices`.
- **4-Question Model-vs-Service Rubric**: Keep database queries, external I/O (Bcrypt, SMTP, CSV), and multi-table transactions in `AuthService`, `VotingService`, and `TabulationService`; keep pure single-object checks (`get_state()`, `is_open()`, `is_editable()`, `has_voted()`, `validate_choices()`) on the ORM models.
- **Atomic One-Shot Submission**: Vote submission must lock `voter_eligibility` (`SELECT ... FOR UPDATE`), verify `voted_at IS NULL`, insert 1 `AnonymousBallot` + *N* `BallotChoice` rows, and set `voted_at = NOW()` in one transaction.

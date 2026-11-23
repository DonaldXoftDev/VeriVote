# Contributing to VeriVote

## Branching & Pull Request Workflow
1. Always pull the latest `main` before starting a task:
   ```bash
   git checkout main && git pull origin main
   ```
2. Create a descriptive feature branch:
   ```bash
   git checkout -b feat/sprint1-auth-module
   ```
3. Commit small, focused changes with clear messages.
4. Run linting and tests before pushing:
   ```bash
   ruff check .
   pytest
   ```
5. Push your branch and open a Pull Request against `main`:
   ```bash
   git push -u origin feat/sprint1-auth-module
   ```

## Architectural Rules
- **Ballot Secrecy Air-Gap**: Never add a `voter_id` or foreign key linking `voter_eligibility` to `anonymous_votes`.
- **Atomic Transactions**: Any vote submission must lock `voter_eligibility` (`SELECT ... FOR UPDATE`), verify `has_voted == False`, insert `anonymous_votes`, and set `has_voted = True` in one transaction.
- **Frontend**: Keep HTML5/Tailwind CSS/Vanilla JS clean and modular under `frontend/`.

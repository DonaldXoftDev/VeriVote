import uuid

from sqlalchemy.orm import Session


class VotingService:
    """Election, Accreditation & Atomic Voting Module (Sprints 1–2).

    Handles CSV email-roster ingestion, SMTP single-use OTP dispatch/verification,
    and one-shot atomic ballot submission (`SELECT ... FOR UPDATE` on
    `voter_eligibility`, inserting 1 `AnonymousBallot` + N `BallotChoice` rows).
    """

    @staticmethod
    def import_csv_roster(db: Session, election_id: uuid.UUID, csv_content: str) -> int:
        raise NotImplementedError("Scheduled for Sprint 1")

    @staticmethod
    def request_otp(db: Session, election_id: uuid.UUID, email: str) -> None:
        raise NotImplementedError("Scheduled for Sprint 1")

    @staticmethod
    def cast_atomic_ballot(db: Session, voting_token: str, payload: dict) -> str:
        """Lock voter_eligibility, verify voted_at IS NULL, insert ballot, return receipt_hash."""
        raise NotImplementedError("Scheduled for Sprint 2")

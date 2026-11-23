import uuid

from sqlalchemy.orm import Session


class TabulationService:
    """Multi-Algorithm Tabulation Module (Sprints 3–4).

    Handles timestamp-driven result unsealing at `end_time`, direct frequency
    counts (SINGLE / MULTI), multi-round Instant-Runoff elimination (RANKED),
    and public receipt_hash inclusion verification.
    """

    @staticmethod
    def compute_direct_tally(db: Session, question_id: uuid.UUID) -> list[dict]:
        raise NotImplementedError("Scheduled for Sprint 3")

    @staticmethod
    def compute_instant_runoff_rcv(db: Session, question_id: uuid.UUID) -> list[dict]:
        raise NotImplementedError("Scheduled for Sprint 3")

    @staticmethod
    def verify_receipt(db: Session, election_id: uuid.UUID, receipt_hash: str) -> bool:
        raise NotImplementedError("Scheduled for Sprint 3")

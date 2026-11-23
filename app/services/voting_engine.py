import uuid

from sqlalchemy.orm import Session


class TabulationAndVotingEngine:
    """Service interface for atomic anonymous vote casting and multi-rule tabulation.

    Sprint 0 defines the architectural boundary; full implementations are scheduled for:
    - Sprint 2: `cast_atomic_vote` (SELECT ... FOR UPDATE + AnonymousVote insert)
    - Sprint 3: `compute_plurality_or_multi` and `compute_instant_runoff_rcv`
    """

    @staticmethod
    def cast_atomic_vote(db: Session, token: str, payload: dict) -> str:
        """Validate ballot, lock voter row, record anonymous vote, return receipt hash."""
        raise NotImplementedError("Scheduled for Sprint 2")

    @staticmethod
    def compute_plurality_or_multi(db: Session, question_id: uuid.UUID) -> list[dict]:
        """Compute direct counts for SINGLE and MULTI ballot questions."""
        raise NotImplementedError("Scheduled for Sprint 3")

    @staticmethod
    def compute_instant_runoff_rcv(db: Session, question_id: uuid.UUID) -> list[dict]:
        """Compute round-by-round Instant-Runoff elimination for RANKED questions."""
        raise NotImplementedError("Scheduled for Sprint 3")

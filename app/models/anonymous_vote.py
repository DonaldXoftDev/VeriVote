import uuid

from sqlalchemy import ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AnonymousVote(Base):
    """Secret ballot box record (table: anonymous_votes).

    ARCHITECTURAL AIR-GAP: Contains zero foreign keys or references to
    `voter_eligibility`, guaranteeing cryptographic unlinkability between
    voter identity and cast preferences.
    """

    __tablename__ = "anonymous_votes"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    election_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("elections.id"),
        nullable=False,
        index=True,
    )
    question_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("ballot_questions.id"),
        nullable=False,
        index=True,
    )
    option_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("candidate_options.id"),
        nullable=False,
        index=True,
    )
    rank_position: Mapped[int | None] = mapped_column(Integer, nullable=True)
    receipt_hash: Mapped[str] = mapped_column(String(64), nullable=False, index=True)

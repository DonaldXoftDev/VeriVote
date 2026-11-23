import uuid

from sqlalchemy import CheckConstraint, ForeignKey, Integer, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class BallotChoice(Base):
    """Individual selection or rank on a cast anonymous ballot (table: ballot_choices)."""

    __tablename__ = "ballot_choices"
    __table_args__ = (
        CheckConstraint(
            "rank_position IS NULL OR rank_position >= 1",
            name="ck_bc_rank_positive",
        ),
        UniqueConstraint("ballot_id", "question_id", "option_id", name="uq_bc_ballot_q_option"),
        UniqueConstraint("ballot_id", "question_id", "rank_position", name="uq_bc_ballot_q_rank"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ballot_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("anonymous_ballots.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    question_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("ballot_questions.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    option_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("candidate_options.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    rank_position: Mapped[int | None] = mapped_column(Integer, nullable=True)

    ballot: Mapped["AnonymousBallot"] = relationship(  # noqa: F821
        back_populates="choices"
    )

import uuid

from sqlalchemy import ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class AnonymousBallot(Base):
    """Secret ballot paper record (table: anonymous_ballots).

    ARCHITECTURAL AIR-GAP: Contains zero voter_id and zero timestamps,
    guaranteeing cryptographic unlinkability between voter identity and cast ballots.
    """

    __tablename__ = "anonymous_ballots"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    election_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("elections.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    receipt_hash: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)

    choices: Mapped[list["BallotChoice"]] = relationship(  # noqa: F821
        back_populates="ballot",
        cascade="all, delete-orphan",
    )

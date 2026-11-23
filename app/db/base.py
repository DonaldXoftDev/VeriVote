from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""


# Import all models here so Alembic autogenerate discovers every table.
from app.models import (  # noqa: E402, F401
    AnonymousVote,
    BallotQuestion,
    CandidateOption,
    Election,
    ElectionOrganizer,
    VoterEligibility,
)

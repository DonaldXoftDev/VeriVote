from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""


# Import all 8 3NF models so Alembic autogenerate discovers every table.
from app.models import (  # noqa: E402, F401
    AnonymousBallot,
    AuditLog,
    BallotChoice,
    BallotQuestion,
    CandidateOption,
    Election,
    User,
    VoterEligibility,
)

from enum import StrEnum


class UserRole(StrEnum):
    """Platform user roles."""

    SUPER_ADMIN = "SUPER_ADMIN"
    ORGANIZER = "ORGANIZER"


class ElectionState(StrEnum):
    """Timestamp-derived election lifecycle states."""

    DRAFT = "DRAFT"
    UPCOMING = "UPCOMING"
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"
    CANCELLED = "CANCELLED"


class RuleType(StrEnum):
    """Voting rule assigned to a ballot question."""

    SINGLE = "SINGLE"
    MULTI = "MULTI"
    RANKED = "RANKED"

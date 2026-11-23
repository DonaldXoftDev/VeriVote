from enum import StrEnum


class AuthMode(StrEnum):
    """Voter accreditation mode for an election."""

    CSV_ROSTER = "CSV_ROSTER"
    DOMAIN_OTP = "DOMAIN_OTP"


class ElectionStatus(StrEnum):
    """Lifecycle states of an election."""

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

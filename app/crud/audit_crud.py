import uuid
from typing import Any

from sqlalchemy.orm import Session

from app.models import AuditLog


class AuditLogCRUD:
    """Append-only CRUD operations for the `audit_logs` table."""

    def create_log(
        self,
        db: Session,
        *,
        user_id: uuid.UUID | None,
        action: str,
        target_type: str | None = None,
        target_id: uuid.UUID | None = None,
        details: dict[str, Any] | None = None,
    ) -> AuditLog:
        """Insert an immutable audit log entry and flush (never commit)."""
        raise NotImplementedError("Scheduled for Sprint 1A implementation")


audit_crud = AuditLogCRUD()

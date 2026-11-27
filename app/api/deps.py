import uuid

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import ForbiddenError, UnauthorizedError
from app.core.security import decode_access_token
from app.db.session import get_db
from app.models import User
from app.models.enums import UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


def get_current_user(
    db: Session = Depends(get_db),
    token: str | None = Depends(oauth2_scheme),
) -> User:
    """Resolve and validate the authenticated user from a Bearer JWT."""
    if not token:
        raise UnauthorizedError("Authentication credentials were not provided.")

    payload = decode_access_token(token)
    raw_sub = payload.get("sub")
    try:
        user_id = uuid.UUID(str(raw_sub))
    except ValueError as exc:
        raise UnauthorizedError("Invalid token subject.") from exc

    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user is None:
        raise UnauthorizedError("User account no longer exists.")

    if not user.is_active:
        raise ForbiddenError("Account is pending approval or has been suspended.")

    return user


def require_super_admin(current_user: User = Depends(get_current_user)) -> User:
    """Ensure the authenticated user holds the SUPER_ADMIN role."""
    if current_user.role != UserRole.SUPER_ADMIN:
        raise ForbiddenError("Super-Admin privileges are required for this action.")
    return current_user


def require_active_organizer(current_user: User = Depends(get_current_user)) -> User:
    """Ensure the authenticated user is an active ORGANIZER (or SUPER_ADMIN)."""
    if current_user.role not in (UserRole.ORGANIZER, UserRole.SUPER_ADMIN):
        raise ForbiddenError("Organizer privileges are required for this action.")
    return current_user


__all__ = [
    "get_current_user",
    "get_db",
    "oauth2_scheme",
    "require_active_organizer",
    "require_super_admin",
]

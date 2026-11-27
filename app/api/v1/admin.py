import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_super_admin
from app.models import User
from app.schemas.error import ErrorResponse
from app.schemas.user import UserResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get(
    "/organizers",
    response_model=list[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="List Election Organizers",
    description=(
        "Retrieve all registered Election Organizer accounts, optionally filtered by "
        "activation status (`is_active`). Requires `SUPER_ADMIN` role."
    ),
    responses={
        401: {"model": ErrorResponse, "description": "Missing or invalid Bearer token."},
        403: {"model": ErrorResponse, "description": "Super-Admin privileges required."},
    },
)
def list_organizers(
    is_active: bool | None = Query(default=None, description="Filter by activation state."),
    db: Session = Depends(get_db),
    _admin: User = Depends(require_super_admin),
) -> list[UserResponse]:
    organizers = AuthService.list_organizers(db=db, is_active=is_active)
    return [UserResponse.model_validate(org) for org in organizers]


@router.patch(
    "/organizers/{user_id}/activate",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Activate an Organizer account",
    description=(
        "Approve a pending or suspended Election Organizer (`is_active=True`) and "
        "record the event in `audit_logs`. Requires `SUPER_ADMIN` role."
    ),
    responses={
        401: {"model": ErrorResponse, "description": "Missing or invalid Bearer token."},
        403: {"model": ErrorResponse, "description": "Super-Admin privileges required."},
        404: {"model": ErrorResponse, "description": "Organizer account not found."},
    },
)
def activate_organizer(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
    admin: User = Depends(require_super_admin),
) -> UserResponse:
    user = AuthService.activate_organizer(db=db, admin=admin, organizer_id=user_id)
    return UserResponse.model_validate(user)


@router.patch(
    "/organizers/{user_id}/suspend",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Suspend an Organizer account",
    description=(
        "Suspend an Election Organizer (`is_active=False`) and record the event in "
        "`audit_logs`. Requires `SUPER_ADMIN` role."
    ),
    responses={
        401: {"model": ErrorResponse, "description": "Missing or invalid Bearer token."},
        403: {"model": ErrorResponse, "description": "Super-Admin privileges required."},
        404: {"model": ErrorResponse, "description": "Organizer account not found."},
    },
)
def suspend_organizer(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
    admin: User = Depends(require_super_admin),
) -> UserResponse:
    user = AuthService.suspend_organizer(db=db, admin=admin, organizer_id=user_id)
    return UserResponse.model_validate(user)

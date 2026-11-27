from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models import User
from app.schemas.error import ErrorResponse
from app.schemas.user import LogoutUser, TokenResponse, UserCreate, UserLogin, UserResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register an Election Organizer",
    description=(
        "Create a new Election Organizer account with `is_active=False`. "
        "A Super-Admin must activate the account before login is permitted."
    ),
    responses={
        409: {"model": ErrorResponse, "description": "Email is already registered."},
        422: {"model": ErrorResponse, "description": "Validation error."},
    },
)
def register_organizer(
    payload: UserCreate,
    db: Session = Depends(get_db),
) -> UserResponse:
    user = AuthService.register_organizer(db=db, payload=payload)
    return UserResponse.model_validate(user)


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Authenticate and obtain JWT",
    description="Verify email and password and return a Bearer JWT for active accounts.",
    responses={
        401: {"model": ErrorResponse, "description": "Invalid email or password."},
        403: {"model": ErrorResponse, "description": "Account pending approval or suspended."},
        422: {"model": ErrorResponse, "description": "Validation error."},
    },
)
def login(
    payload: UserLogin,
    db: Session = Depends(get_db),
) -> TokenResponse:
    return AuthService.login(db=db, payload=payload)


@router.post(
    "/logout",
    response_model=LogoutUser,
    status_code=status.HTTP_200_OK,
    summary="Log out current user",
    description="Acknowledge client-side logout for the authenticated session.",
    responses={
        401: {"model": ErrorResponse, "description": "Missing or invalid Bearer token."},
        403: {"model": ErrorResponse, "description": "Inactive or suspended account."},
    },
)
def logout(
    current_user: User = Depends(get_current_user),
) -> LogoutUser:
    return AuthService.logout(current_user=current_user)


@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current authenticated user",
    description="Return the profile of the currently authenticated active user.",
    responses={
        401: {"model": ErrorResponse, "description": "Missing or invalid Bearer token."},
        403: {"model": ErrorResponse, "description": "Inactive or suspended account."},
    },
)
def get_me(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    return UserResponse.model_validate(current_user)

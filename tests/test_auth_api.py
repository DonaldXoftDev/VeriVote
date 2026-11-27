import pytest
from fastapi.testclient import TestClient


@pytest.mark.skip(reason="Pending AuthService implementation")
def test_register_endpoint_returns_201_and_omits_password_hash(client: TestClient) -> None:
    """POST /api/v1/auth/register -> 201 Created with UserResponse."""
    _ = client


@pytest.mark.skip(reason="Pending AuthService implementation")
def test_register_duplicate_email_returns_409_error_response(client: TestClient) -> None:
    """POST /api/v1/auth/register -> 409 Conflict with ErrorResponse envelope."""
    _ = client


@pytest.mark.skip(reason="Pending AuthService implementation")
def test_login_endpoint_returns_200_token_response(client: TestClient) -> None:
    """POST /api/v1/auth/login -> 200 OK with Bearer JWT and user profile."""
    _ = client


@pytest.mark.skip(reason="Pending AuthService implementation")
def test_get_me_requires_valid_bearer_token(client: TestClient) -> None:
    """GET /api/v1/auth/me -> 401 without token, 200 with active user token."""
    _ = client


@pytest.mark.skip(reason="Pending AuthService implementation")
def test_logout_endpoint_returns_200_logout_message(client: TestClient) -> None:
    """POST /api/v1/auth/logout -> 200 OK with LogoutUser payload."""
    _ = client

import pytest
from fastapi.testclient import TestClient


@pytest.mark.skip(reason="Pending AuthService implementation")
def test_list_organizers_requires_super_admin_role(client: TestClient) -> None:
    """GET /api/v1/admin/organizers -> 401 unauthenticated, 403 for organizer, 200 for admin."""
    _ = client


@pytest.mark.skip(reason="Pending AuthService implementation")
def test_activate_organizer_endpoint_approves_account(client: TestClient) -> None:
    """PATCH /api/v1/admin/organizers/{user_id}/activate -> 200 OK with is_active=True."""
    _ = client


@pytest.mark.skip(reason="Pending AuthService implementation")
def test_suspend_organizer_endpoint_revokes_access(client: TestClient) -> None:
    """PATCH /api/v1/admin/organizers/{user_id}/suspend -> 200 OK with is_active=False."""
    _ = client


@pytest.mark.skip(reason="Pending AuthService implementation")
def test_activate_missing_organizer_returns_404(client: TestClient) -> None:
    """PATCH /api/v1/admin/organizers/{unknown_id}/activate -> 404 NotFoundError."""
    _ = client

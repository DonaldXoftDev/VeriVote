from fastapi.testclient import TestClient


def test_health_endpoint(client: TestClient) -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["app"] == "VeriVote"
    assert payload["database"] == "connected"


def test_root_serves_static_frontend(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "VeriVote" in response.text
    assert "{{" not in response.text


def test_dashboard_placeholder_served(client: TestClient) -> None:
    response = client.get("/dashboard.html")
    assert response.status_code == 200
    assert "Account Approved" in response.text

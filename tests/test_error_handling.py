from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

from app.core.error_handlers import register_exception_handlers
from app.core.exceptions import (
    ConflictError,
    ForbiddenError,
    NotFoundError,
    UnauthorizedError,
)


def _create_error_test_app() -> FastAPI:
    test_app = FastAPI()
    register_exception_handlers(test_app)

    class SampleBody(BaseModel):
        count: int

    @test_app.get("/conflict")
    def trigger_conflict() -> None:
        raise ConflictError("Email already registered.", details={"field": "email"})

    @test_app.get("/forbidden")
    def trigger_forbidden() -> None:
        raise ForbiddenError("Account pending approval.", error_code="ACCOUNT_INACTIVE")

    @test_app.get("/unauthorized")
    def trigger_unauthorized() -> None:
        raise UnauthorizedError("Invalid token.")

    @test_app.get("/not-found")
    def trigger_not_found() -> None:
        raise NotFoundError("Organizer not found.")

    @test_app.post("/validate")
    def trigger_validation(body: SampleBody) -> SampleBody:
        return body

    @test_app.get("/boom")
    def trigger_unhandled() -> None:
        raise RuntimeError("sensitive internal detail")

    return test_app


def test_verivote_error_defaults_code_to_class_name() -> None:
    client = TestClient(_create_error_test_app())
    response = client.get("/conflict")
    assert response.status_code == 409
    assert response.json() == {
        "error": {
            "code": "ConflictError",
            "message": "Email already registered.",
            "details": {"field": "email"},
        }
    }


def test_verivote_error_allows_custom_code_override() -> None:
    client = TestClient(_create_error_test_app())
    response = client.get("/forbidden")
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "ACCOUNT_INACTIVE"


def test_unauthorized_and_not_found_errors() -> None:
    client = TestClient(_create_error_test_app())
    assert client.get("/unauthorized").status_code == 401
    assert client.get("/not-found").status_code == 404


def test_request_validation_error_uses_error_response_envelope() -> None:
    client = TestClient(_create_error_test_app())
    response = client.post("/validate", json={"count": "not-an-int"})
    assert response.status_code == 422
    body = response.json()
    assert body["error"]["code"] == "RequestValidationError"
    assert isinstance(body["error"]["details"], list)


def test_unhandled_exception_hides_internal_details() -> None:
    client = TestClient(_create_error_test_app(), raise_server_exceptions=False)
    response = client.get("/boom")
    assert response.status_code == 500
    body = response.json()
    assert body["error"]["code"] == "InternalServerError"
    assert "sensitive internal detail" not in response.text

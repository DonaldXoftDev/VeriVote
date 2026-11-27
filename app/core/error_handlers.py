import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.exceptions import VeriVoteBaseError
from app.schemas.error import ErrorDetail, ErrorResponse

logger = logging.getLogger(__name__)


def _build_error_response(
    *,
    status_code: int,
    code: str,
    message: str,
    details: object | None = None,
) -> JSONResponse:
    payload = ErrorResponse(
        error=ErrorDetail(
            code=code,
            message=message,
            details=details,
        )
    )
    return JSONResponse(status_code=status_code, content=payload.model_dump())


def register_exception_handlers(app: FastAPI) -> None:
    """Register centralized exception handlers on the FastAPI application."""

    @app.exception_handler(VeriVoteBaseError)
    async def verivote_error_handler(
        _request: Request,
        exc: VeriVoteBaseError,
    ) -> JSONResponse:
        return _build_error_response(
            status_code=exc.status_code,
            code=exc.error_code,
            message=exc.message,
            details=exc.details,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(
        _request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        return _build_error_response(
            status_code=422,
            code="RequestValidationError",
            message="Request validation failed.",
            details=exc.errors(),
        )

    @app.exception_handler(Exception)
    async def unhandled_error_handler(
        _request: Request,
        exc: Exception,
    ) -> JSONResponse:
        logger.exception("Unhandled server error: %s", exc)
        return _build_error_response(
            status_code=500,
            code="InternalServerError",
            message="An unexpected internal error occurred.",
            details=None,
        )

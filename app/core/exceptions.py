from typing import Any


class VeriVoteBaseError(Exception):
    """Base application exception for all domain and HTTP errors in VeriVote.

    By default, `error_code` uses the raised exception's class name
    (e.g. `ConflictError`, `ForbiddenError`), unless overridden explicitly.
    """

    status_code: int = 500

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        error_code: str | None = None,
        details: Any | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.error_code = error_code or self.__class__.__name__
        self.details = details


class BadRequestError(VeriVoteBaseError):
    """400 Bad Request."""

    status_code = 400


class UnauthorizedError(VeriVoteBaseError):
    """401 Unauthorized."""

    status_code = 401


class ForbiddenError(VeriVoteBaseError):
    """403 Forbidden."""

    status_code = 403


class NotFoundError(VeriVoteBaseError):
    """404 Not Found."""

    status_code = 404


class ConflictError(VeriVoteBaseError):
    """409 Conflict."""

    status_code = 409


class UnprocessableEntityError(VeriVoteBaseError):
    """422 Unprocessable Entity."""

    status_code = 422

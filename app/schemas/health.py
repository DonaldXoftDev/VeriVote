from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Health check response payload."""

    status: str
    app: str
    version: str
    environment: str
    database: str

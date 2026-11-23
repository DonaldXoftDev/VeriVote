from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.v1.router import api_router
from app.core.config import get_settings

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    settings = get_settings()

    application = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=(
            "Customizable Web-Based Electronic Voting System supporting Single-Choice, "
            "Multiple-Choice, and Ranked-Choice (Instant-Runoff) ballots with a 3NF "
            "8-table schema and decoupled voter anonymity."
        ),
        docs_url="/docs",
        redoc_url="/redoc",
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(api_router, prefix="/api/v1")

    if FRONTEND_DIR.exists():
        application.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")
        templates = Jinja2Templates(directory=str(FRONTEND_DIR))

        @application.get("/", include_in_schema=False, response_class=HTMLResponse)
        def serve_frontend(request: Request) -> HTMLResponse:
            return templates.TemplateResponse(
                request=request,
                name="index.html",
                context={"app_name": settings.APP_NAME, "version": settings.APP_VERSION},
            )

    return application


app = create_app()

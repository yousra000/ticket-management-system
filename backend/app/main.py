import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import OperationalError

from . import models  # noqa: F401  (registers the Ticket model with Base)
from .config import settings
from .database import Base, engine
from .routes.health import router as health_router
from .routes.tickets import router as tickets_router

logger = logging.getLogger("ticket_api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create the table if it does not exist. The API still starts if MySQL is
    # down; /api/health then reports the problem instead of crashing the app.
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database table verified")
    except OperationalError:
        logger.exception("Could not reach the database at startup")
    yield


app = FastAPI(
    title="Ticket Management API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type"],
)

app.include_router(health_router)
app.include_router(tickets_router)


@app.exception_handler(OperationalError)
async def database_unavailable_handler(request: Request, exc: OperationalError):
    logger.error("Database error on %s %s: %s", request.method, request.url.path, exc.orig)
    return JSONResponse(
        status_code=503,
        content={"detail": "Database is unavailable. Check that MySQL is running and DATABASE_URL is correct."},
    )

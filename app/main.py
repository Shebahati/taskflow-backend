import logging
from fastapi import FastAPI

from app.core.logging import setup_logging
from app.core.middleware import RequestLoggingMiddleware

# 1) configure logging first
setup_logging()
logger = logging.getLogger("taskflow")

# 2) now import routers (after logging is ready)
from app.api.auth import router as auth_router
from app.api.users import router as users_router


app = FastAPI(title="TaskFlow API", version="0.1.0")

@app.on_event("startup")
def on_startup() -> None:
    logger.info("App starting up")

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.add_middleware(RequestLoggingMiddleware)

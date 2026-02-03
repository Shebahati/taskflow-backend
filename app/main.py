from fastapi import FastAPI
from app.api.auth import router as auth_router

app = FastAPI(title="TaskFlow API", version="0.1.0")

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}

app.include_router(auth_router, prefix="/auth", tags=["auth"])

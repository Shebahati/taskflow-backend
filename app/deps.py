from typing import Dict
from fastapi import Header, HTTPException, status
from app.services.jwt_service import decode_access_token

def get_current_user(authorization: str | None = Header(default=None)) -> Dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    token = authorization.removeprefix("Bearer ").strip()

    try:
        payload = decode_access_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    return {
        "id": int(payload["sub"]),
        "email": payload["email"],
        "full_name": payload["full_name"],
    }

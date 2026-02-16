import time
from typing import Dict

import jwt

from app.core.config import settings


def create_access_token(user: Dict) -> str:
    payload = {
        "sub": str(user["id"]),
        "email": user["email"],
        "full_name": user["full_name"],
        "exp": int(time.time()) + settings.JWT_EXPIRE_SECONDS,
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)


def decode_access_token(token: str) -> Dict:
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])

import time
import jwt
from typing import Dict

JWT_SECRET = "dev-secret-change-me"
JWT_ALG = "HS256"
JWT_EXPIRE_SECONDS = 60 * 60  # 1 hour

def create_access_token(user: Dict) -> str:
    payload = {
        "sub": str(user["id"]),
        "email": user["email"],
        "full_name": user["full_name"],
        "exp": int(time.time()) + JWT_EXPIRE_SECONDS,
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)

def decode_access_token(token: str) -> Dict:
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])

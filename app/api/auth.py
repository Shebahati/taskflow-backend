from fastapi import APIRouter, status
from app.schemas.auth import RegisterRequest, RegisterResponse
from pydantic import BaseModel, EmailStr
from app.services.jwt_service import create_access_token

router = APIRouter()

_fake_id_counter = 0

@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest) -> RegisterResponse:
    global _fake_id_counter
    _fake_id_counter += 1

    # TODO: later -> save to DB + hash password
    return RegisterResponse(
        id=_fake_id_counter,
        email=payload.email,
        full_name=payload.full_name,
    )

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/login")
def login(payload: LoginRequest) -> dict:
    # TODO later: validate against DB
    fake_user = {"id": 1, "email": str(payload.email), "full_name": "Current User"}
    token = create_access_token(fake_user)
    return {"access_token": token, "token_type": "bearer"}
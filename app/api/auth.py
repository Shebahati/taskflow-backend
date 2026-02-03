from fastapi import APIRouter, status
from app.schemas.auth import RegisterRequest, RegisterResponse

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

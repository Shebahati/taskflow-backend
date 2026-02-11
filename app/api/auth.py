from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from app.db.deps import get_db
from app.db.models import User
from app.schemas.user import RegisterRequest, UserPublic
from app.services.password_service import hash_password
from app.services.jwt_service import create_access_token

router = APIRouter()

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> UserPublic:
    # 1) check email unique
    stmt = select(User).where(User.email == str(payload.email))
    existing = db.execute(stmt).scalar_one_or_none()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # 2) create user
    user = User(
        email=str(payload.email),
        full_name=payload.full_name,
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return UserPublic(id=user.id, email=user.email, full_name=user.full_name)

@router.post("/login")
def login(payload: LoginRequest) -> dict:
    # TODO: next step -> real login with DB + verify_password
    fake_user = {"id": 1, "email": str(payload.email), "full_name": "Current User"}
    token = create_access_token(fake_user)
    return {"access_token": token, "token_type": "bearer"}

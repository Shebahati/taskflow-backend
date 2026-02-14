from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from app.db.deps import get_db
from app.db.models import User
from app.schemas.user import RegisterRequest, UserPublic
from app.services.password_service import hash_password, verify_password
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
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> dict:
    stmt = select(User).where(User.email == str(payload.email))
    user = db.execute(stmt).scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    token = create_access_token(
        {"id": user.id, "email": user.email, "full_name": user.full_name}
    )
    return {"access_token": token, "token_type": "bearer"}

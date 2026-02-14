from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.db.models import User
from app.schemas.user import UserPublic

router = APIRouter()

@router.get("/me", response_model=UserPublic)
def get_me(current_user: User = Depends(get_current_user)) -> UserPublic:
    return UserPublic(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
    )

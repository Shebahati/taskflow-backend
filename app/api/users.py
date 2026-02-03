from fastapi import APIRouter, Depends
from app.deps import get_current_user

router = APIRouter()

@router.get("/me")
def get_me(current_user: dict = Depends(get_current_user)) -> dict:
    return {
        "id": 1,
        "email": "me@example.com",
        "full_name": "Current User",
    }

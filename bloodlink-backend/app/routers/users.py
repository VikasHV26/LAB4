from fastapi import APIRouter, Depends
from app.middleware.auth_middleware import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me")
def get_me(current_user: dict = Depends(get_current_user)):
    return {
        "message": "Authenticated",
        "user": current_user
    }
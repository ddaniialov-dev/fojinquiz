from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import APIRouter

from quiz_project import get_db
from user_app import schemas
from user_app.crud import UserManager


router = APIRouter(prefix="/users",
        tags=["users"],
        responses={404: {"description": "Not found"}}
    )

@router.post("/", response_model=schemas.User, tags=["users"])
def create_user(
    user: schemas.UserCreate, 
    db: Session = Depends(get_db)
):
    user_manager = UserManager(db)
    db_user = user_manager.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return user_manager.create_user(user=user)

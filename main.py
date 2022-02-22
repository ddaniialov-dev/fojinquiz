from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from quiz_project import database
from user_app import models, schemas
from user_app.crud import UserManager



models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/", response_model=models.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_manager = UserManager(db)
    user = user_manager.get_user_by_email(email=user.email)
    if user:
        raise HTTPException(status_code=400, detail="User already registered")
    return user_manager.create_user(user=user)


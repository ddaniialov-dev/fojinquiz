from sqlalchemy.orm import Session

from user_app import models, schemas
import hashlib, uuid


class UserManager:
    
    def __init__(self, database: Session):
        self.db = database

    def get_user(self, user_id:int):
        return self.db.query(models.User).filter(models.User.id == user_id).first()

    def get_user_by_email(self, email: str):
        return self.db.query(models.User).filter(models.User.email == email).first()
    
    def get_users(self, skip: int = 0, limit: int = 100):
        return self.db.query(models.User).offset(skip).limit(limit).all()
    
    def create_user(self, user: schemas.UserCreate):
        salt = uuid.uuid4().hex.encode()
        password = user.password.encode()
        hashed_password = hashlib.sha512(password + salt).hexdigest()
        db_user = models.User(email=user.email, hashed_password=hashed_password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

from sqlalchemy.orm import Session

import models


class UserManager:
    
    def __init__(self, database: Session):
        self.db = database

    def get_user(self, user_id:int):
        return self.db.query(models.User).filter(models.User.id == user_id).first()

    def get_user_by_email(self, email: str):
        return self.db.query(models.User)
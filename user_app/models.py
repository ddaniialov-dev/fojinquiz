from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship

from quiz_project import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    tests = relationship("Test")
    sessions = relationship("Session")

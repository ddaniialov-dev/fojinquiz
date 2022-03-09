from sqlalchemy import Boolean, Column, String, Integer
from sqlalchemy.orm import relationship

from quiz_project import AbstractBaseModel


class User(AbstractBaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean)
    tests = relationship("Test")
    sessions = relationship("Session")


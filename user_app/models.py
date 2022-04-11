from sqlalchemy import Boolean, Column, String, Integer
from sqlalchemy.orm import relationship, backref

from quiz_project.behaviours.base_model import AbstractBaseModel


class User(AbstractBaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    tests = relationship("Test", backref=backref("holder", lazy="joined"))
    sessions = relationship("Session", backref=backref("user", lazy="joined"))

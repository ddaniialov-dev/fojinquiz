from sqlalchemy import Boolean, Column, Integer, String

from quiz_project.behaviours.base_model import BaseModel


class Test(BaseModel):
    __tablename__ = "tests"
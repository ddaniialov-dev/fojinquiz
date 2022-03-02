from sqlalchemy import Column, Integer, DateTime

from quiz_project import Base
from quiz_project.utils import get_current_time


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), default=get_current_time)
    updated_at = Column(DateTime(timezone=True), nullable=True, onupdate=get_current_time)

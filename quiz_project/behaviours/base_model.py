from sqlalchemy import Column, Integer, DateTime
<<<<<<< HEAD
from sqlalchemy.orm import Session
=======
>>>>>>> implement_test_architecture

from quiz_project import Base
from quiz_project.utils import get_current_time


class BaseModel(Base):
    __abstract__ = True
<<<<<<< HEAD
    
=======

>>>>>>> implement_test_architecture
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), default=get_current_time)
    updated_at = Column(DateTime(timezone=True), nullable=True, onupdate=get_current_time)

from datetime import datetime

import pytz
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import Session

from quiz_project import Base


class BaseModel(Base):
    __abstract__ = True
    
    def __init__(self, *args, **kwargs):
        self.__init__(*args, **kwargs)
        self.session = Session()
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(tz=pytz.timezone("UTC")))
    updated_at = Column(DateTime(timezone=True), nullable=True)

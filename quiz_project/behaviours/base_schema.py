from datetime import datetime

from pydantic import BaseModel


class BaseSchema(BaseModel):
    id: int = None
    created_date: datetime = None
    updated_date: datetime = None
    
    class Config:
        orm_mode = True

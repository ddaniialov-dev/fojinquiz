from datetime import datetime

from pydantic import BaseModel, Field


class BaseSchema(BaseModel):
    id: int = Field(default=None, hidden=True)
    created_date: datetime = Field(default=None, hidden=True)
    updated_date: datetime = Field(default=None, hidden=True)
    
    class Config:
        orm_mode = True

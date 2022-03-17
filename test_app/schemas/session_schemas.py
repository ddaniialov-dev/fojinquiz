from datetime import datetime

from pydantic import BaseModel


class GetSession(BaseModel):
    finished_date: datetime = None
    user: int = None
    test: int = None

    class Config:
        orm_mode = True


class CreateSession(BaseModel):
    user: int | None = None
    test: int | None = None

    class Config:
        orm_mode = True

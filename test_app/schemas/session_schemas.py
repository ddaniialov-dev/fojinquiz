from typing import List

from datetime import datetime

from pydantic import BaseModel

from test_app.schemas.question_schemas import GetQuestion


class GetSession(BaseModel):
    id: int
    finished_date: datetime = None
    user_id: int = None
    test_id: int = None
    questions: List[GetQuestion]

    class Config:
        orm_mode = True


class CreateSession(BaseModel):
    user_id: int | None = None
    test_id: int | None = None
    questions: List[GetQuestion] = []

    class Config:
        orm_mode = True

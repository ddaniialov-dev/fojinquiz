from pydantic import BaseModel

from test_app.schemas import GetQuestion
from test_app.schemas.answer_scheme import GetAnswer


class GetUserAnswer(BaseModel):
    answer_id: int
    session_id: int

    class Config:
        orm_mode = True


class CreateUserAnswer(BaseModel):
    answer_id: int

    class Config:
        orm_mode = True


class GetUserAnswers(BaseModel):
    session_id: int
    user_id: int
    answer: GetAnswer
    question: GetQuestion
    right_answer: GetAnswer

    class Config:
        orm_mode = True

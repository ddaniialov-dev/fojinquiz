from pydantic import BaseModel


class GetUserAnswer(BaseModel):
    answer_id: int
    session_id: int

    class Config:
        orm_mode = True


class CreateUserAnswer(BaseModel):
    answer_id: int

    class Config:
        orm_mode = True

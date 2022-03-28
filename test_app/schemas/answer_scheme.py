from pydantic import BaseModel

class CreateAnswer(BaseModel):
    question: int
    text: str
    is_true: bool = False

    class Config:
        orm_mode = True

class GetAnswer(BaseModel):
    id: int
    question: int
    text: str
    is_true: bool

    class Config:
        orm_mode = True

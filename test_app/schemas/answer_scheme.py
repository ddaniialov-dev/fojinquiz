from pydantic import BaseModel

class CreateAnswer(BaseModel):
    text: str
    is_true: bool = False

    class Config:
        orm_mode = True

class UpdateAnswer(BaseModel):
    text: str | None
    is_true: bool | None

    class Config:
        orm_mode = True

class GetAnswer(BaseModel):
    id: int
    text: str
    is_true: bool

    class Config:
        orm_mode = True

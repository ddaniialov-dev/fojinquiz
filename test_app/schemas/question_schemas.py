from pydantic import BaseModel


class GetQuestion(BaseModel):
    id: int
    text: str

    class Config:
        orm_mode = True


class CreateQuestion(BaseModel):
    text: str

    class Config:
        orm_mode = True


class UpdateQuestion(BaseModel):
    text: str | None

    class Config:
        orm_mode = True


class ImageSchema(BaseModel):
    path: str
    content_type: str
    question: int

    class Config:
        orm_mode = True

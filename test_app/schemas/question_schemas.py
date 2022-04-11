from pydantic import BaseModel


class GetQuestion(BaseModel):
    id: int
    test_id: int
    text: str

    class Config:
        orm_mode = True


class CreateQuestion(BaseModel):
    test_id: int
    text: str

    class Config:
        orm_mode = True


class UpdateQuestion(BaseModel):
    test_id: int
    text: str

    class Config:
        orm_mode = True


class ImageSchema(BaseModel):
    path: str
    content_type: str
    question: int

    class Config:
        orm_mode = True

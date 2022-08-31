from datetime import datetime

from pydantic import BaseModel, validator

from test_app.schemas.question_schemas import GetQuestion


class GetTest(BaseModel):
    id: int
    holder_id: int
    published: bool = True
    duration: int | None
    created_at: datetime
    modified_at: datetime | None
    title: str | None
    questions: list[GetQuestion] | list

    class Config:
        orm_mode = True


class UpdateTest(BaseModel):
    holder_id: int | None
    title: str | None
    published: bool | None
    duration: int | None

    class Config:
        orm_mode = True

    @validator('duration')
    def postive_field(cls, value):
        if value < 0:
            raise ValueError('Duration is not positive')
        return value


class CreateTest(BaseModel):
    holder_id: int | None
    title: str | None
    published: bool | None = True
    duration: int

    class Config:
        orm_mode = True

    @validator('duration')
    def postive_field(cls, value):
        if value < 0:
            raise ValueError('Duration is not positive')
        return value


class ImageSchema(BaseModel):
    path: str
    content_type: str
    question: int

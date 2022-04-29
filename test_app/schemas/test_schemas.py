from datetime import datetime

from pydantic import BaseModel

from test_app.schemas.question_schemas import GetQuestion


class GetTest(BaseModel):
    id: int
    holder_id: int
    published: bool = True
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
    title: str | None

    class Config:
        orm_mode = True


class CreateTest(BaseModel):
    holder_id: int = None
    title: str | None = None
    published: bool | None = True
    title: str | None

    class Config:
        orm_mode = True


class ImageSchema(BaseModel):
    path: str
    content_type: str
    question: int

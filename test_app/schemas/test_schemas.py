from datetime import datetime

from pydantic import BaseModel


class GetTest(BaseModel):
    id: int
    holder_id: int
    published: bool = True
    created_at: datetime
    modified_at: datetime | None

    class Config:
        orm_mode = True


class UpdateTest(BaseModel):
    holder_id: int | None
    title: str | None
    published: bool | None

    class Config:
        orm_mode = True


class CreateTest(BaseModel):
    holder_id: int = None
    title: str | None = None
    published: bool | None = True

    class Config:
        orm_mode = True


class ImageSchema(BaseModel):
    path: str
    content_type: str
    question: int

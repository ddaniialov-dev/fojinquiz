from pydantic import BaseModel


class TestSchema(BaseModel):
    holder: str | None
    published: bool


class ImageSchema(BaseModel):
    path: str
    content_type: str
    question: int

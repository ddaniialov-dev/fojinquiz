from datetime import datetime

from pydantic import BaseModel


class TestSchema(BaseModel):
    holder: int = None
    published: bool = True


class UpdateTestSchema(BaseModel):
    title: str | None
    published: bool = True
    holder: int | None
    published_date: datetime | None

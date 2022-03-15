from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from quiz_project.behaviours import BaseSchema


class TestSchema(BaseSchema):
    holder: int = None
    published: bool = True


class UpdateTestSchema(BaseModel):
    title: Optional[str]
    published: bool = True
    holder: Optional[int]
    published_date: Optional[datetime]
    
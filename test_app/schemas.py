from pydantic import BaseModel


class TestSchema(BaseModel):
    holder: str | None
    published: bool

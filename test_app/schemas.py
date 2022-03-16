from datetime import datetime

from pydantic import BaseModel


class TestGet(BaseModel):
    id: int
    holder: int
    published: bool = True
    created_at: datetime
    modified_at: datetime | None
    
    class Config:
        orm_mode = True


class TestUpdate(BaseModel):
    holder: int | None
    title: str | None
    published: bool | None

    class Config:
        orm_mode = True


class TestCreate(BaseModel):
    holder: int = None
    title: str | None = None
    published: bool | None = True

    class Config:
        orm_mode = True

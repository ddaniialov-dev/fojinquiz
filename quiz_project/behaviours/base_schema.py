from pydantic import BaseModel


class BaseSchema(BaseModel):
    id: int

    class Config:
        orm_mode = True

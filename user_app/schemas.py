from pydantic import BaseModel


class BaseUser(BaseModel):
    username: str
    

class UserCreate(BaseUser):
    password: str


class User(BaseUser):
    id: int
    is_active: bool
    
    class Config:
        orm_mode = True

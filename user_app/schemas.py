from pydantic import validator
from quiz_project.behaviours import BaseSchema


class BaseUser(BaseSchema):
    username: str


class UserCreate(BaseUser):
    password: str

    @validator(
        'username',
        'password',
        check_fields=False, 
        always=True
    )
    def blank_string(cls, value):
        if not value:
            raise ValueError('Can not be used')
        return value


class UserSchema(BaseUser):
    id: int = None
    is_active: bool
    
    
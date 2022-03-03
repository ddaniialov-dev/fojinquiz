from quiz_project.behaviours import BaseSchema


class BaseUser(BaseSchema):
    username: str


class UserCreate(BaseUser):
    password: str


class UserSchema(BaseUser):
    id: int = None
    is_active: bool

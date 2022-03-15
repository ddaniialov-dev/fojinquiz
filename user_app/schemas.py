from pydantic import validator, BaseModel


class UserGet(BaseModel):
    id: int
    username: str
    is_active: bool


class UserCreate(BaseModel):
    username: str
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

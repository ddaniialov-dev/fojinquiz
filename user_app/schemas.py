from pydantic import validator, BaseModel


class UserGet(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True

    @validator(
        "username",
        "password",
    )
    def blank_string(cls, value):
        if not value:
            raise ValueError("Can not be used")
        return value


class UserCreate(BaseModel):
    username: str
    password: str
    email: str

    class Config:
        orm_mode = True

    @validator(
        "username",
        "password",
        "email",
    )
    def blank_string(cls, value):
        if not value:
            raise ValueError("Can not be used")
        return value

    @validator("email")
    def check_email(cls, v: str):
        if not v.endswith("@fojin.tech"):
            raise ValueError("Email does not match")
        return v

#
# class UserAdminCreate(BaseModel):
#     username: str
#     password: str
#     email: str
#     is_admin: bool
#
#     class Config:
#         orm_mode = True
#
#     @validator(
#         "username",
#         "password",
#         "email",
#     )
#     def blank_string(cls, value):
#         if not value:
#             raise ValueError("Can not be used")
#         return value
#
#     @validator("email")
#     def check_email(cls, v: str):
#         if not v.endswith("@fojin.tech"):
#             raise ValueError("Email does not match")
#         return v
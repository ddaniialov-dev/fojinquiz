from datetime import datetime

import pytz
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_jwt_auth import AuthJWT

import user_app


def get_current_time() -> datetime:
    return datetime.now(tz=pytz.timezone("UTC"))


async def get_current_user(db_session: AsyncSession, auth: AuthJWT):
    async with user_app.crud.UserManager(db_session) as user_manager:
        user = await user_manager.get_user_by_username(auth.get_jwt_subject())
    return user[0]


def save_file(file_path: str, byte_data: bytes) -> None:
    with open(file_path, mode='wb') as file:
        file.write(byte_data)

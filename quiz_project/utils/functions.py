import pytz
import aiofiles
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_jwt_auth import AuthJWT
from fastapi import Depends

import user_app
from .dependencies import token_header


def get_current_time() -> datetime:
    return datetime.now(tz=pytz.timezone("UTC"))


async def get_current_user(
    db_session: AsyncSession,
    auth: AuthJWT = Depends(),
    token_auth = Depends(token_header)    
):
    async with user_app.crud.UserManager(db_session) as user_manager:
        user = await user_manager.get_user_by_username(auth.get_jwt_subject())
    return user[0]


async def get_file(file_path: str) -> bytes:
    async with aiofiles.open(file_path, mode='rb') as file:
        byte_data = await file.read()

    return byte_data


async def save_file(file_path: str, byte_data: bytes) -> None:
    async with aiofiles.open(file_path, mode='wb') as file:
        await file.write(byte_data)

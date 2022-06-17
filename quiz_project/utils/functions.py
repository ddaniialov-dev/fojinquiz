import hashlib
from datetime import datetime
from uuid import NAMESPACE_X500, uuid5

import aiofiles
import pytz


def get_current_time() -> datetime:
    return datetime.now(tz=pytz.timezone("UTC"))


async def get_file(file_path: str) -> bytes:
    async with aiofiles.open(file_path, mode="rb") as file:
        byte_data = await file.read()

    return byte_data


async def save_file(file_path: str, byte_data: bytes) -> None:
    async with aiofiles.open(file_path, mode="wb") as file:
        await file.write(byte_data)


def hash_password(username, password):
    salt = uuid5(NAMESPACE_X500, username).hex.encode()
    password = password.encode()
    hashed_password = hashlib.sha512(password + salt).hexdigest()
    return hashed_password

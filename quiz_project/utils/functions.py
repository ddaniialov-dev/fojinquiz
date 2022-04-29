import pytz
import aiofiles
from datetime import datetime


def get_current_time() -> datetime:
    return datetime.now(tz=pytz.timezone("UTC"))


async def get_file(file_path: str) -> bytes:
    async with aiofiles.open(file_path, mode="rb") as file:
        byte_data = await file.read()

    return byte_data


async def save_file(file_path: str, byte_data: bytes) -> None:
    async with aiofiles.open(file_path, mode="wb") as file:
        await file.write(byte_data)

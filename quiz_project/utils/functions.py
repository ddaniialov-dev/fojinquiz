import pytz

from datetime import datetime


def get_current_time() -> datetime:
    return datetime.now(tz=pytz.timezone("UTC"))


def save_file(file_path: str, byte_data: bytes) -> None:
    with open(file_path, mode='wb') as file:
        file.write(byte_data)

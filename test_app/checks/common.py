from quiz_project.database import Base
from fastapi import HTTPException


async def check_if_exist(objects: list[Base]) -> None:
    if not objects:
        raise HTTPException(
                status_code=404, detail='Items not found.'
            )


async def check_if_holder(user_id: int, holder_id: int) -> None:
    if user_id != holder_id:
        raise HTTPException(
                status_code=403, detail='Permission Denied.'
            )


async def check_if_exists(object: Base) -> None:
    if not object:
        raise HTTPException(
                status_code=404, detail='Item not found.'
            )

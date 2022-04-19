from test_app.models import Test
from fastapi import HTTPException
from test_app.crud import TestManager

from user_app.models import User


async def check_for_tests(tests: list[Test]):
    if not tests:
        raise HTTPException(
                status_code=404, detail='Tests not found.'
            )


async def get_test_or_not_found(manager: TestManager, test_id: int):
    test = await manager.get_test(test_id)
    if not test:
        raise HTTPException(
                status_code=404, detail='Test not found.'
            )
    return test


async def check_for_holder(manager: TestManager, user: User, test_id: int):
    test = await manager.get_test(test_id)
    if test.holder_id != user.id:
        raise HTTPException(
                status_code=403, detail='Permission Denied.'
            )

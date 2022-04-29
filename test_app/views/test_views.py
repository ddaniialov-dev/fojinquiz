from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException
from user_app.crud import UserManager

from user_app.models import User

from quiz_project.database import get_session
from quiz_project.utils.dependencies import get_current_user

from test_app.crud import TestManager
from test_app.schemas import GetTest, CreateTest, UpdateTest
from test_app.checks.common import check_if_holder, check_if_exist, check_if_exists

test_router = APIRouter(
    prefix='/tests',
    tags=['tests'],
)


@test_router.get(
    '/',
    status_code=200,
    response_model=list[GetTest]
)
async def get_user_tests(
    database_session: AsyncSession = Depends(get_session),
    auth: User = Depends(get_current_user)
) -> list[GetTest]:
    async with TestManager(database_session) as manager:
        tests = await manager.get_user_tests(auth.id)
    return tests


@test_router.get(
    '/all/',
    status_code=200,
    response_model=list[GetTest]
)
async def get_all_tests(
    database_session: AsyncSession = Depends(get_session)
) -> list[GetTest]:
    async with TestManager(database_session) as manager:
        tests = await manager.get_tests()
        await check_if_exists(tests)
        return tests


@test_router.post(
    '/',
    status_code=201,
    response_model=GetTest
)
async def create_test(
    test: CreateTest,
    database_session: AsyncSession = Depends(get_session),
    auth: User = Depends(get_current_user)
) -> GetTest:
    async with UserManager(database_session) as manager:
        user = await manager.get_user(auth.id)
        if not user.is_admin:
            raise HTTPException(
                status_code=403, detail="You need to be an administrator to create tests!"
            )
    async with TestManager(database_session) as manager:
        test.holder_id = auth.id
        result = await manager.create_test(test)
        if not result:
            raise HTTPException(
                status_code=400, detail='Test wat not created'
            )
        return result


@test_router.get(
    '/{test_id}/',
    response_model=GetTest,
    status_code=200
)
async def get_test(
    test_id: int,
    database_session: AsyncSession = Depends(get_session)
):
    async with TestManager(database_session) as manager:
        test = await manager.get_test(test_id)
        await check_if_exists(test)
        return test


@test_router.put(
    '/{test_id}/',
    response_model=UpdateTest,
    status_code=200
)
async def update_test(
    test_id: int,
    test: UpdateTest,
    database_session: AsyncSession = Depends(get_session),
    auth: User = Depends(get_current_user)
):
    async with TestManager(database_session) as manager:
        test_object = await get_test(test_id, database_session)
        await check_if_holder(auth.id, test_object.holder_id)
        test = await manager.update_test(
            test_id,
            test.dict(exclude={"holder_id"}, exclude_unset=True)
        )
        return test


@test_router.delete(
    '/{test_id}/',
    status_code=204,
)
async def delete_test(
    test_id: int,
    database_session: AsyncSession = Depends(get_session),
    auth: User = Depends(get_current_user)
) -> Response:
    async with TestManager(database_session) as manager:
        test_object = await get_test(test_id, database_session)
        await check_if_holder(auth.id, test_object.holder_id)
        await manager.delete_test(auth, test_id)
        return Response(status_code=204)

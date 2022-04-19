from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException

from user_app.models import User

from quiz_project.database import get_session
from quiz_project.utils.dependencies import get_current_user

from test_app.crud import TestManager
from test_app.schemas import GetTest, CreateTest, UpdateTest
from test_app.checks import check_for_holder, check_for_tests, get_test_or_not_found

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
    async with TestManager(database_session) as test_manager:
        tests = await test_manager.get_user_tests(auth.id)
        await check_for_tests(tests)
    return tests


@test_router.get(
    '/all/',
    status_code=200,
    response_model=list[GetTest]
)
async def get_all_tests(
    database_session: AsyncSession = Depends(get_session)
) -> list[GetTest]:
    async with TestManager(database_session) as test_manager:
        tests = await test_manager.get_tests()
        await check_for_tests(tests)
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
    async with TestManager(database_session) as test_manager:
        test.holder_id = auth.id
        result = await test_manager.create_test(test)
        if not result:
            raise HTTPException(
                status_code=400, detail='Test wat not created'
            )
    return result


@test_router.delete(
    '/{test_id}/',
    status_code=204,
)
async def delete_test(
    test_id: int,
    database_session: AsyncSession = Depends(get_session),
    auth: User = Depends(get_current_user)
) -> Response:
    async with TestManager(database_session) as test_manager:
        await get_test_or_not_found(test_manager, test_id)
        await check_for_holder(test_manager, auth, test_id)

        tests = await test_manager.delete_test(auth, test_id)
        await check_for_tests(tests)

        return Response(status_code=204)


@test_router.get(
    '/{test_id}/',
    response_model=GetTest,
    status_code=200
)
async def get_test(
    test_id: int,
    database_session: AsyncSession = Depends(get_session)
):
    async with TestManager(database_session) as test_manager:
        test = await get_test_or_not_found(test_manager, test_id)
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
    async with TestManager(database_session) as test_manager:
        await get_test_or_not_found(test_manager, test_id)
        await check_for_holder(test_manager, auth, test_id)
        test = await test_manager.update_test(
            test_id,
            test.dict(exclude={"holder_id"}, exclude_unset=True)
        )
        await check_for_tests(test)
        return test

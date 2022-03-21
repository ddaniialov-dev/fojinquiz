from typing import List

from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException

from test_app.crud import TestManager
from quiz_project import (
    get_session,
    get_current_user,
)
from test_app.schemas import GetTest, CreateTest, UpdateTest
from user_app.models import User

test_router = APIRouter(
    prefix='/tests',
    tags=['tests'],
)


@test_router.get(
    '/',
    status_code=200,
    response_model=List[GetTest]
)
async def get_user_tests(
    database_session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user)
) -> List[GetTest]:
    async with TestManager(database_session) as test_manager:
        tests = await test_manager.get_user_tests(user.id)

        if not tests:
            raise HTTPException(
                status_code=404, detail='data not found'
            )

    return tests


@test_router.get(
    '/all/',
    status_code=200,
    response_model=List[GetTest]
)
async def get_all_tests(
    database_session: AsyncSession = Depends(get_session)
) -> List[GetTest]:
    async with TestManager(database_session) as test_manager:
        tests = await test_manager.get_tests()

        if not tests:
            raise HTTPException(
                status_code=404, detail='data not found'
            )

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
        test.holder = auth.id
        result = await test_manager.create_test(test)
        if not result:
            raise HTTPException(
                status_code=400, detail='test wat not created'
            )
    return result


@test_router.delete(
    '/{test_id}/',
    status_code=204,
)
async def delete_test(
    test_id: int,
    database_session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user)
) -> Response:
    async with TestManager(database_session) as test_manager:
        result = await test_manager.delete_test(user, test_id)

    if not result:
        raise HTTPException(status_code=404, detail="data not found")

    return Response()


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
        result = await test_manager.get_test(test_id)

    if not result:
        raise HTTPException(
            status_code=404, detail="data not found"
        )
    return result


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
        test.holder = auth.id
        result = await test_manager.update_test(auth, test_id, test.dict())

    if not result:
        raise HTTPException(
            status_code=404, detail="data not found"
        )
    return result

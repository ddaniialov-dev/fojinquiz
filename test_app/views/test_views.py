from typing import List

from fastapi import Response
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException

from test_app.crud import TestManager
from quiz_project import (
    get_session,
    token_header,
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
    auth: AuthJWT = Depends(),
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
        auth: AuthJWT = Depends(),
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
    auth: AuthJWT = Depends(),
    database_session: AsyncSession = Depends(get_session),
    user: User = Depends()
) -> GetTest:
    async with TestManager(database_session) as test_manager:
        test.holder = user.id
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
    auth: AuthJWT = Depends(),
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
        auth: AuthJWT = Depends(),
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
    auth: AuthJWT = Depends(),
    database_session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user)
):
    async with TestManager(database_session) as test_manager:
        user = await get_current_user(database_session, auth)
        test.holder = user.id
        result = await test_manager.update_test(user, test_id, test.dict())

    if not result:
        raise HTTPException(
            status_code=404, detail="data not found"
        )
    return result


question_router = APIRouter(
    prefix='/questions',
    tags=['questions'],
    dependencies=[Depends(token_header)]
)


@question_router.post(
    '/questions/'
)
async def get_questions():
    pass

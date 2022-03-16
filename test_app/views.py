from typing import List

from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, Response

from .crud import TestManager
from quiz_project import (JwtAccessRequired, get_session,
                          token_header, get_current_user)
from test_app.schemas import TestGet, TestCreate, TestUpdate


router = APIRouter(
    prefix='/tests',
    tags=['tests'],
    dependencies=[Depends(token_header)]
)


@router.get(
    '/',
    status_code=200,
    response_model=List[TestGet]
)
@JwtAccessRequired()
async def get_user_tests(
    auth: AuthJWT = Depends(),
    database_session: AsyncSession = Depends(get_session)
) -> List[TestGet]:
    user = await get_current_user(database_session, auth)
    async with TestManager(database_session) as test_manager:
        tests = await test_manager.get_user_tests(user.id)

        if not tests:
            raise HTTPException(
                status_code=404, detail='data not found'
            )

    return tests


@router.get(
    '/all/',
    status_code=200,
    response_model=List[TestGet]
)
@JwtAccessRequired()
async def get_all_tests(
    auth: AuthJWT = Depends(),
    database_session: AsyncSession = Depends(get_session)
) -> List[TestGet]:
    async with TestManager(database_session) as test_manager:
        tests = await test_manager.get_tests()

        if not tests:
            raise HTTPException(
                status_code=404, detail='data not found'
            )

    return tests


@router.post(
    '/',
    status_code=201,
    response_model=TestGet
)
@JwtAccessRequired()
async def create_test(
    test: TestCreate,
    auth: AuthJWT = Depends(),
    database_session: AsyncSession = Depends(get_session)
) -> int:
    user = await get_current_user(database_session, auth)
    async with TestManager(database_session) as test_manager:
        test.holder = user.id
        result = await test_manager.create_test(test)
        if not result:
            raise HTTPException(
                status_code=400, detail='test wat not created'
            )
    return result


@router.delete(
    '/{test_id}/',
    status_code=204,
)
@JwtAccessRequired()
async def delete_test(
    test_id: int,
    auth: AuthJWT = Depends(),
    database_session: AsyncSession = Depends(get_session)
) -> None:
    user = await get_current_user(database_session, auth)
    async with TestManager(database_session) as test_manager:
        result = await test_manager.delete_test(user, test_id)

    if not result:
        raise HTTPException(status_code=404, detail="data not found")

    return Response()


@router.get(
    '/{test_id}/',
    status_code=200
)
@JwtAccessRequired()
async def get_test(
   test_id: int,
   auth: AuthJWT = Depends(),
   database_session: AsyncSession = Depends(get_session)
):
    async with TestManager(database_session) as test_manager:
        result =  await test_manager.get_test(test_id)
    
    if not result:
        raise HTTPException(
            status_code=404, detail="data not found"
        )
    return result


@router.put(
    '/{test_id}/',
    response_model=TestUpdate,
    status_code=200
)
async def update_test(
    test_id: int,
    test: TestUpdate,
    auth: AuthJWT = Depends(),
    database_session: AsyncSession = Depends(get_session)
):
    user = await get_current_user(database_session, auth)
    test.holder = user.id
    async with TestManager(database_session) as test_manager:
        result =  await test_manager.update_test(user, test_id, test.dict())
    
    if not result:
        raise HTTPException(
            status_code=404, detail="data not found"
        )
    return result

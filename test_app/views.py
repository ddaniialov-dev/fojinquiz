from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT

from sqlalchemy.ext.asyncio import AsyncSession

from test_app.schemas import TestSchema, UpdateTestSchema

from quiz_project import JwtAccessRequired, get_session, token_header
from user_app import UserManager
from .crud import TestManager
from quiz_project import get_current_user

router = APIRouter(
    prefix='/tests',
    tags=['tests'],
    dependencies=[Depends(token_header)]
)


@router.get(
    '/',
    status_code=200,
    response_model=List[TestSchema]
)
@JwtAccessRequired()
async def get_tests(
    auth: AuthJWT = Depends(),
    database_session: AsyncSession = Depends(get_session)
) -> List[TestSchema]:
    user = await get_current_user(database_session, auth)
    async with TestManager(database_session) as test_manager:
        tests = await test_manager.get_tests(user)

        if not tests:
            raise HTTPException(
                status_code=404, detail='data not found'
            )

    return tests


@router.post(
    '/',
    status_code=201,
    response_model=TestSchema
)
@JwtAccessRequired()
async def create_test(
    test: TestSchema,
    auth: AuthJWT = Depends(),
    database_session: AsyncSession = Depends(get_session)
) -> int:
    user = get_current_user(database_session, auth)
    async with TestManager(database_session) as test_manager:
        test.holder = user[0].id
        record_id = await test_manager.create_test(test)

        if not record_id:
            raise HTTPException(
                status_code=400, detail='test wat not created'
            )

    return record_id


@router.delete(
    '/{test_id}/',
    status_code=204
)
@JwtAccessRequired()
async def delete_test(
    test_id: int,
    auth: AuthJWT = Depends(),
    database_session: AsyncSession = Depends(get_session)
) -> None:
    user = get_current_user(database_session, auth)
    async with TestManager(database_session) as test_manager:
        await test_manager.delete_test(user, test_id)

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
    user = await get_current_user(database_session, auth)
    async with TestManager(database_session) as test_manager:
        result =  await test_manager.get_test(test_id)
    
    if not result:
        raise HTTPException(
            status_code=404, detail="data not found"
        )
    return result


@router.put(
    '/{test_id}/',
    response_model=UpdateTestSchema,
    status_code=200
)
async def update_test(
    test_id: int,
    test: UpdateTestSchema,
    auth: AuthJWT = Depends(),
    database_session: AsyncSession = Depends(get_session)
):
    user = await get_current_user(database_session, auth)
    test.holder = user.id
    async with TestManager(database_session) as test_manager:
        result =  await test_manager.update_test(user, test_id, test.dict())
    return result 
from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT

from sqlalchemy.ext.asyncio import AsyncSession

from test_app.schemas import TestSchema

from quiz_project import JwtAccessRequired, get_session, token_header

from .crud import TestManager

router = APIRouter(
    prefix='/tests',
    tags=['tests'],
    dependencies=[Depends(token_header)]
)


@router.get('/', status_code=200)
@JwtAccessRequired()
async def get_tests(
    auth: AuthJWT = Depends(),
    database_session: AsyncSession = Depends(get_session)
):
    async with TestManager(database_session) as test_manager:
        tests = await test_manager.get_tests()

        if not tests:
            raise HTTPException(
                status_code=404, detail='data not found'
            )

    return tests


@router.post('/', status_code=201)
@JwtAccessRequired()
async def create_test(
    test: TestSchema,
    auth: AuthJWT = Depends(),
    database_session: AsyncSession = Depends(get_session)
):
    async with TestManager(database_session) as test_manager:
        record_id = await test_manager.create_test(test)

        if not record_id:
            return HTTPException(
                status_code=400, detail='test wat not created'
            )

    return record_id


@router.delete('/{test_id}/', status_code=204)
@JwtAccessRequired()
async def delete_test(
    test_id: int,
    auth: AuthJWT = Depends(),
    database_session: AsyncSession = Depends(get_session)
) -> None:
    async with TestManager(database_session) as test_manager:
        await test_manager.delete_test(test_id)

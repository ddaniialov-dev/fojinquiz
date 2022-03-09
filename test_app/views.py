from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT

from sqlalchemy.ext.asyncio import AsyncSession

from test_app.schemas import TestSchema

from quiz_project import JwtAccessRequired, get_session, token_header

from .crud import TestManager

router = APIRouter(
    prefix="/tests",
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
        data = await test_manager.get_tests()
        return data

    raise HTTPException(
        status_code=404, detail='data not found'
    )


@router.post('/', status_code=201)
# @JwtAccessRequired()
async def create_test(
    test: TestSchema,
    auth: AuthJWT = Depends(),
    database_session: AsyncSession = Depends(get_session)
):
    async with TestManager(database_session) as test_manager:
        await test_manager.create_test(test)


@router.delete('/', status_code=204)
# @JwtAccessRequired()
async def delete_test(
    test: TestSchema,
    auth: AuthJWT = Depends(),
    database_session: AsyncSession = Depends(get_session)
):
    async with TestManager(database_session) as test_manager:
        await test_manager.delete_test(test.id)

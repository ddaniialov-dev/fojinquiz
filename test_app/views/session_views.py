from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from user_app.models import User

from quiz_project.database import get_session
from quiz_project.utils.dependencies import get_current_user

from test_app.schemas import GetSession
from test_app.crud import SessionManager
from test_app.checks.common import check_if_exists, check_if_exist


session_router = APIRouter(
    prefix='/tests/{test_id}/sessions',
    tags=['sessions'],
)


@session_router.post(
    '/',
    status_code=201,
    response_model=GetSession
)
async def create_sesion(
    test_id: int,
    auth: User = Depends(get_current_user),
    database_session: AsyncSession = Depends(get_session)
):
    async with SessionManager(database_session) as session_manager:
        test_object = await session_manager.get_test(test_id)
        await check_if_exists(test_object)
        session_object = await session_manager.create_session(test_object.id, auth)
        return session_object


@session_router.get(
    path='/',
    status_code=200,
    response_model=list[GetSession]
)
async def get_sessions(
    auth: User = Depends(get_current_user),
    database_session: AsyncSession = Depends(get_session)
):
    async with SessionManager(database_session) as session_manager:
        session_objects = await session_manager.get_sessions(auth.id)
        await check_if_exist(session_objects)
        return session_objects
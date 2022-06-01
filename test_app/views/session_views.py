from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from quiz_project.database import get_session
from test_app.schemas import GetSession
from test_app.crud import SessionManager
from test_app.checks.common import check_if_exists
from test_app.checks.sessions import check_if_test_has_session

session_router = APIRouter(
    prefix="/tests/{test_id}/sessions",
    tags=["sessions"],
)


@session_router.post("/", status_code=201, response_model=GetSession)
async def create_session(
    test_id: int,
    request: Request,
    database_session: AsyncSession = Depends(get_session),
):
    async with SessionManager(database_session) as manager:
        test_object = await manager.get_test(test_id)
        await check_if_exists(test_object)
        session_object = await manager.create_session(test_object.id, request.user)
        return session_object


@session_router.get("/", status_code=200, response_model=list[GetSession])
async def get_sessions(
    test_id: int,
    request: Request,
    database_session: AsyncSession = Depends(get_session),
):
    async with SessionManager(database_session) as manager:
        test_object = await manager.get_test(test_id)
        await check_if_exists(test_object)
        session_objects = await manager.get_sessions(request.user.id, test_id)
        return session_objects


@session_router.get("/{session_id}/", status_code=200, response_model=GetSession)
async def get_session(
    test_id: int,
    session_id: int,
    request: Request,
    database_session: AsyncSession = Depends(get_session),
):
    async with SessionManager(database_session) as manager:
        test_object = await manager.get_test(test_id)
        await check_if_exists(test_object)
        session_object = await manager.get_session(request.user.id, session_id)
        await check_if_exists(session_object)
        await check_if_test_has_session(test_id, session_object)
        return session_object

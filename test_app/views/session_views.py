from typing import List

from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException

from user_app.models import User

from quiz_project import get_session
from quiz_project.utils import get_current_user

from test_app.crud import SessionManager
from test_app.schemas import CreateSession, GetSession


session_router = APIRouter(
    prefix='/sessions',
    tags=['sessions'],
)


@session_router.get(
    '/',
    status_code=200,
    response_model=List[GetSession]
)
async def get_user_sessions(
    database_session: AsyncSession = Depends(get_session),
    auth: User = Depends(get_current_user)
) -> List[GetSession]:
    async with SessionManager(database_session) as session_manager:
        sessions = await session_manager.get_sessions(auth.id)

    if not sessions:
        raise HTTPException(
            status_code=404, detail="data not found"
        )

    return sessions


@session_router.post(
    '/',
    status_code=201,
    response_model=GetSession
)
async def create_session(
    session_scheme: CreateSession,
    database_session: AsyncSession = Depends(get_session),
    auth: User = Depends(get_current_user)
) -> GetSession:
    async with SessionManager(database_session) as session_manager:
        session_scheme.user = auth.id
        session_object = await session_manager.create_session(session_scheme)

    return session_object


@session_router.get(
    '/{session_id}/',
    status_code=200,
    response_model=GetSession
)
async def get_session_object(
    session_id: int,
    database_session: AsyncSession = Depends(get_session),
    auth: User = Depends(get_current_user)
):
    async with SessionManager(database_session) as session_manager:
        session = await session_manager.get_session(auth.id, session_id)

    if not session:
        raise HTTPException(
            status_code=404, detail="data not found"
        )

    return session


@session_router.delete(
    '/{session_id}/',
    status_code=204,
)
async def delete_session(
    session_id: int,
    database_session: AsyncSession = Depends(get_session),
    auth: User = Depends(get_current_user)
):
    async with SessionManager(database_session) as session_manager:
        result = await session_manager.delete_session(auth, session_id)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="data not found"
        )

    return Response(status_code=204)

from typing import List

from fastapi import Response
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException

from quiz_project import (
    get_session,
    get_current_user,
    token_header
)
from test_app.schemas import CreateSession, GetSession
from test_app.crud import SessionManager
from user_app.models import User


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
    auth: AuthJWT = Depends(),
    database_session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user)
) -> List[GetSession]:
    async with SessionManager(database_session) as session_manager:
        sessions = await session_manager.get_sessions(user.id)

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
    auth: AuthJWT = Depends(token_header),
    database_session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user)
) -> GetSession:
    async with SessionManager(database_session) as session_manager:
        session_scheme.user = user.id
        session_object = await session_manager.create_session(session_scheme)

    return session_object


@session_router.get(
    '/{session_id}/',
    status_code=200,
    response_model=GetSession
)
async def get_session_object(
    session_id: int,
    auth: AuthJWT = Depends(),
    database_session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user)
):
    async with SessionManager(database_session) as session_manager:
        session = await session_manager.get_session(user.id, session_id)

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
    auth: AuthJWT = Depends(),
    database_session: AsyncSession = Depends(get_session),
    user: User = Depends(get_current_user)
):
    async with SessionManager(database_session) as session_manager:
        result = await session_manager.delete_session(user, session_id)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="data not found"
        )

    return Response(status_code=204)

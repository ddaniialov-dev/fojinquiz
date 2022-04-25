from typing import Callable

from fastapi import Header, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import MissingTokenError, CSRFError

from ..database import get_session
from user_app.crud import UserManager, User




async def get_current_user(
    auth: AuthJWT = Depends(),
    db_session: AsyncSession = Depends(get_session)
) -> User:
    try:
        auth.jwt_required()
    except MissingTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No access token provided.",
        )
    async with UserManager(db_session) as manager:
        user = await manager.get_user_by_username(auth.get_jwt_subject())
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

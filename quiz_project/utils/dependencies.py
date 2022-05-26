from fastapi import HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import MissingTokenError

from ..database import get_session
from user_app.crud import UserManager, User


async def get_current_user(
    auth: AuthJWT = Depends(), db_session: AsyncSession = Depends(get_session)
) -> User:
    pass

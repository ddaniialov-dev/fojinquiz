from fastapi import Header, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import JWTDecodeError

from user_app import UserManager

from quiz_project.database import get_session
from user_app.crud import UserManager


def token_header(authorization: str = Header(...)):
    if not authorization:
        raise HTTPException(
            status_code=400,
            detail='authentication credentials are not provided'
        )


async def get_current_user(
    auth: AuthJWT = Depends(),
    token_auth = Depends(token_header),
    db_session: AsyncSession = Depends(get_session)
):
    try:
        auth.jwt_required()
    except JWTDecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    async with UserManager(db_session) as user_manager:
        user = await user_manager.get_user_by_username(auth.get_jwt_subject())
    if user:
        user = user[0]
    return user

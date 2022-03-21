from fastapi import Header, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_jwt_auth import AuthJWT

import user_app

from quiz_project.database import get_session


def token_header(authorization: str = Header(...)):
    if not authorization:
        raise HTTPException(
            status_code=400,
            detail='authentication credentials are not provided'
        )


async def get_current_user(
    auth: AuthJWT = Depends(),
    token_auth=Depends(token_header),
    db_session: AsyncSession = Depends(get_session)
):
    auth.jwt_required()
    async with user_app.crud.UserManager(db_session) as user_manager:
        user = await user_manager.get_user_by_username(auth.get_jwt_subject())
    user = user[0]
    return user

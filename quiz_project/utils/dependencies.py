from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Header, HTTPException, Depends

from quiz_project.database import get_session
import user_app


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
    auth.jwt_required()
    async with user_app.UserManager(db_session) as user_manager:
        user = await user_manager.get_user_by_username(auth.get_jwt_subject())

    return user[0]

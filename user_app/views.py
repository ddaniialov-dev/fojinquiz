from fastapi import APIRouter, Response, status, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

from sqlalchemy.ext.asyncio import AsyncSession

from quiz_project.database import get_session
from quiz_project.utils.dependencies import get_current_user

from .crud import UserManager
from .schemas import UserGet, UserCreate
from .models import User


user_router = APIRouter(
    tags=['auth'],
)


@user_router.post(
    '/login/',
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
)
async def login(
    user: UserCreate,
    auth: AuthJWT = Depends(),
    database_session: AsyncSession = Depends(get_session)
):
    async with UserManager(database_session) as manager:
        if not await manager.check_user_credentials(user.username, user.password):
            raise HTTPException(
                status_code=401, detail='username/password error'
            )

        return await obtain_auth_tokens(user, auth)


@user_router.post(
    "/register/",
    response_class=JSONResponse,
    status_code=status.HTTP_201_CREATED
)
async def register(
    user: UserCreate,
    database_session: AsyncSession = Depends(get_session)
):
    async with UserManager(database_session) as manager:
        if await manager.get_user_by_username(username=user.username):
            raise HTTPException(
                status_code=400, detail='User already registered'
            )

        user = await manager.create_user(user=user)
        return JSONResponse(content={"detail": "Registered"}, status_code=201)



@user_router.post(
    '/refresh/',
    response_class=JSONResponse,
    status_code=status.HTTP_201_CREATED
)
async def refresh(
    auth: AuthJWT = Depends()
):
    auth.jwt_refresh_token_required()

    user = auth.get_jwt_subject()
    new_access_token = auth.create_access_token(subject=user)
    auth.set_access_cookies(new_access_token)
    return {
        'access_token': new_access_token
    }


@user_router.get(
    '/me/',
    response_model=UserGet,
    status_code=status.HTTP_200_OK
)
async def get_me(
    user: User = Depends(get_current_user)
):
    return user


async def obtain_auth_tokens(user: UserCreate, auth: AuthJWT) -> dict:
    refresh_token = auth.create_refresh_token(subject=user.username, expires_time=False)
    access_token = auth.create_access_token(subject=user.username, expires_time=False)
    auth.set_access_cookies(access_token)
    auth.set_refresh_cookies(refresh_token)
    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }

@user_router.delete('/logout')
def logout(auth: AuthJWT = Depends()):
    """
    Because the JWT are stored in an httponly cookie now, we cannot
    log the user out by simply deleting the cookies in the frontend.
    We need the backend to send us a response to delete the cookies.
    """
    auth.jwt_required()

    auth.unset_jwt_cookies()
    return {"msg":"Successfully logout"}
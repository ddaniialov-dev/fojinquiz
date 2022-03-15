from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from quiz_project import get_session

from .crud import UserManager
from .schemas import UserGet, UserCreate
from quiz_project import JwtAccessRequired

router = APIRouter(
    tags=['auth']
)


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"


@AuthJWT.load_config
def get_config():
    return Settings()


@router.post(
    '/login/',
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
)
async def login(
    user: UserCreate,
    auth: AuthJWT = Depends(),
    database_session: AsyncSession = Depends(get_session)
):
    async with UserManager(database_session) as user_manager:
        if not await user_manager.check_user_credentials(user.username, user.password):
            raise HTTPException(
                status_code=401, detail='username/password error'
            )

        return await obtain_auth_tokens(user, auth)


@router.post(
    "/register/",
    response_class=JSONResponse,
    status_code=status.HTTP_201_CREATED
)
async def register(
    user: UserCreate,
    database_session: AsyncSession = Depends(get_session)
):
    async with UserManager(database_session) as user_manager:
        if await user_manager.get_user_by_username(username=user.username):
            raise HTTPException(
                status_code=400, detail='User already registered'
            )

        user = await user_manager.create_user(user=user)
        token_pair = await obtain_auth_tokens(user, AuthJWT())
        return token_pair

    raise HTTPException(
        status_code=400, detail='Bad Request'
    )


@router.post(
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

    return {
        'access_token': new_access_token
    }


@router.get(
    '/me/',
    response_model=UserGet,
    status_code=status.HTTP_200_OK
)
@JwtAccessRequired()
async def get_me(
    auth: AuthJWT = Depends(),
    database_session: AsyncSession = Depends(get_session)
):
    async with UserManager(database_session) as user_manager:
        user = await user_manager.get_user_by_username(username=auth.get_jwt_subject())
    return UserGet.from_orm(user[0])


async def obtain_auth_tokens(user: UserCreate, auth: AuthJWT) -> dict:
    refresh_token = auth.create_refresh_token(subject=user.username, expires_time=False)
    access_token = auth.create_access_token(subject=user.username, expires_time=False)

    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }

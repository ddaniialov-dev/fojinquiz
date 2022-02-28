from typing import Type

from fastapi import Request, FastAPI
from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from quiz_project import get_database_session

from .crud import UserManager
from .schemas import UserCreate


app = FastAPI()


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"


@AuthJWT.load_config
def get_config():
    return Settings()


@app.exception_handler(AuthJWTException)
async def jwt_exception_handler(request: Request, exc: Type[AuthJWTException]):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            'detail': exc.message
        }
    )


@app.post('/login/')
async def login(
        user: UserCreate,
        auth: AuthJWT = Depends(),
        database_session: AsyncSession = Depends(get_database_session)
):
    user_manager = UserManager(database_session)
    if not await user_manager.check_user_credentials(user.username, user.password):
        raise HTTPException(status_code=401, detail='username/password error')

    return await obtain_auth_tokens(user, auth)


@app.post("/register/")
async def register(
    user: UserCreate,
    database_session: AsyncSession = Depends(get_database_session)
):
    user_manager = UserManager(database_session)

    if await user_manager.get_user_by_username(username=user.username):
        raise HTTPException(status_code=400, detail='User already registered')

    user = await user_manager.create_user(user=user)
    token_pair = await obtain_auth_tokens(user, AuthJWT())
    return token_pair


@app.post('/refresh/')
async def refresh(auth: AuthJWT = Depends()):
    auth.jwt_refresh_token_required()

    user = auth.get_jwt_subject()
    new_access_token = auth.create_access_token(subject=user)

    return {
        'access_token': new_access_token
    }


async def obtain_auth_tokens(user: UserCreate, auth: AuthJWT) -> dict:
    refresh_token = auth.create_refresh_token(subject=user.username)
    access_token = auth.create_access_token(subject=user.username)

    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }


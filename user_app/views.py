from fastapi import  Request, FastAPI
from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from sqlalchemy.ext.asyncio import AsyncSession

from quiz_project import get_database_session
from user_app import schemas
from user_app.crud import UserManager

from .models import User
from .schemas import UserCreate


app = FastAPI()


@app.exception_handler(AuthJWTException)
async def jwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            'detail': exc.message
        }
    )


# @app.post('/login/')
# async def login(user: User, auth: AuthJWT = Depends()):
#     pass


@app.post("/register/", response_model=schemas.User)
async def create_user(
    user: UserCreate,
    database_session: AsyncSession = Depends(get_database_session)
):
    user_manager = UserManager(database_session)
    db_user = await user_manager.get_user_by_username(username=user.username)

    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")

    user = await user_manager.create_user(user=user)
    return user

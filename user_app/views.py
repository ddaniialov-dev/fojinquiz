from fastapi import  Depends, Request, FastAPI
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException
from sqlalchemy.ext.asyncio import AsyncSession

from quiz_project.database import get_session
from user_app import schemas
from user_app.crud import UserManager
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
    db_session: AsyncSession = Depends(get_session)
):
    user_manager = UserManager(db_session)
    db_user = await user_manager.get_user_by_username(username=user.username)

    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")

    user = await user_manager.create_user(user=user)
    return user

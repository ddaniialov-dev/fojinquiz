from time import time
from user_app.schemas import UserGet
import secrets
import time
import os

from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.authentication import AuthenticationBackend, AuthCredentials, UnauthenticatedUser
import jwt
from starlette.requests import HTTPConnection
from user_app.crud import UserManager
from user_app.views import user_router
from quiz_project.conf import SAFE_METHODS, LIFETIME_TOKEN_HOUR
from test_app.views import (
    test_router,
    question_router,
    session_router,
    answer_router,
    user_answer_router,
)

from quiz_project.database import get_session


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(question_router)
app.include_router(test_router)
app.include_router(session_router)
app.include_router(answer_router)
app.include_router(user_answer_router)


@app.middleware("http")
async def csrf_validatior(request: Request, call_next):

    if request.method in SAFE_METHODS:
        response = await call_next(request)
        if not request.headers.get("X-CSRF"):
            csrf = secrets.token_hex(32)
            response.set_cookie(key="CSRF", value=csrf)
            response.headers["X-CSRF"] = csrf
    else:
        header_csrf = request.headers.get("X-CSRF")
        if header_csrf:
            cookies_csrf = request.cookies.get("CSRF")
            if not cookies_csrf:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Cookies hasn't CSRF."}
                )
            if cookies_csrf == header_csrf:
                response = await call_next(request)
                return response
            else:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "CSRF is not valid."}
                )
        return JSONResponse(
            status_code=401,
            content={"detail": "CSRF is missing."}
        )
    return response


class JWTAuthBackend(AuthenticationBackend):

    async def authenticate(self, conn):
        token = conn.cookies.get('access_token_cookie')

        path = str(conn.scope.get('path')).replace('/', '')
        paths = ['register', 'login']

        if token:
            token_decode = jwt.decode(token, os.getenv("SECRET_KEY"))
            now = int(time.time())

            timeout_token = token_decode.get('iat') \
                + LIFETIME_TOKEN_HOUR * 60 * 60

            if token_decode.get('nbf') > now > timeout_token:
                raise HTTPException(
                    status_code=401,
                    detail={'error': "JWT timeout."}
                )

            database_session = await get_session()
            async with UserManager(database_session) as manager:
                user = await manager.get_user_by_username(token_decode.get('sub'))

            if user:
                return AuthCredentials(), user
            else:
                raise HTTPException(
                    status_code=401,
                    detail={'error': "JWT live but user not found."}
                )

        elif path not in paths:
            raise HTTPException(
                status_code=401,
                detail={
                    'error': 'JWT not found.',
                    'description': "This is an exceptional error. You weren't supposed to see her."
                }
            )


class JWTAuthMiddleware(AuthenticationMiddleware):
    async def __call__(self, scope, receive, send) -> None:
        try:
            await super().__call__(scope, receive, send)
            conn = HTTPConnection(scope)
        except HTTPException as exc:
            conn = HTTPConnection(scope)
            response = self.on_error(conn, exc)
            await response(scope, receive, send)
            return

    @staticmethod
    def default_on_error(conn: HTTPConnection, exc: Exception):
        return JSONResponse(content={"detail": exc.detail}, status_code=403)


app.add_middleware(JWTAuthMiddleware, backend=JWTAuthBackend())

import secrets

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from quiz_project.conf import SAFE_METHODS
from user_app.views import user_router
from test_app.views import (
    test_router,
    question_router,
    session_router,
    answer_router,
    user_answer_router,
)


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
            response.set_cookie(key='CSRF', value=csrf)
            response.headers['X-CSRF'] = csrf
    else:
        header_csrf = request.headers.get("X-CSRF")
        if header_csrf:
            cookies_csrf = request.cookies.get("CSRF")
            if not cookies_csrf:
                return JSONResponse(status_code=401, content={"detail": "Cookies hasn't CSRF."})
            if cookies_csrf == header_csrf:
                response = await call_next(request)
                return response
            else:
                return JSONResponse(status_code=401, content={"detail": "CSRF is not valid."})
        return JSONResponse(status_code=401, content={"detail": "CSRF is missing."})

    return response

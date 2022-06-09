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


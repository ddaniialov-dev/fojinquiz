from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from user_app.views import user_router
from quiz_project.middlewares import csrf_validatior_deep, JWTAuthBackend, JWTAuthMiddleware
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


@app.middleware("http")
async def csrf_validatior(request: Request, call_next):
    return await csrf_validatior_deep(request, call_next)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    JWTAuthMiddleware,
    backend=JWTAuthBackend()
)

app.include_router(user_router)
app.include_router(question_router)
app.include_router(test_router)
app.include_router(session_router)
app.include_router(answer_router)
app.include_router(user_answer_router)

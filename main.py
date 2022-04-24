from fastapi import FastAPI

from user_app.views import user_router
from test_app.views import (
    test_router,
    question_router,
    session_router,
    answer_router,
    user_answer_router,
)

app = FastAPI()


app.include_router(user_router)
app.include_router(question_router)
app.include_router(test_router)
app.include_router(session_router)
app.include_router(answer_router)

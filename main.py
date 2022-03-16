from fastapi import FastAPI

from user_app import router as user_app_router
from test_app import test_router, question_router

app = FastAPI()


app.include_router(user_app_router)
app.include_router(test_router)
app.include_router(question_router)

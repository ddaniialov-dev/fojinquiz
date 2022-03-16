from fastapi import FastAPI

from user_app.views import router as user_app_router
from test_app.views import test_router as test_app_router

app = FastAPI()


app.include_router(user_app_router)
app.include_router(test_app_router)

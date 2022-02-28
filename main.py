from fastapi import FastAPI

from user_app.views import router as user_app_router

app = FastAPI()


app.include_router(user_app_router)

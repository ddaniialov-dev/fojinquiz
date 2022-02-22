from fastapi import FastAPI

from user_app import models, views
from quiz_project import database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


app.include_router(views.router)

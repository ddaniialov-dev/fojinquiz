from fastapi import FastAPI


import user_app
from quiz_project import database

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


app.include_router(user_app.views.router)

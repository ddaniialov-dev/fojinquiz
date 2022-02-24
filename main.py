from fastapi import FastAPI

from user_app.views import app as user_app


app = FastAPI()

app.mount('/', user_app)

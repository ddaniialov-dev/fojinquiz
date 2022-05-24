import os

from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi_jwt_auth import AuthJWT

load_dotenv()


class Settings:
    DB = {
        "USER": os.getenv("POSTGRES_USER"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "NAME": os.getenv("POSTGRES_DB"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
    }
    DATABASE_URL = (
        f"postgresql+asyncpg://{DB['USER']}:{DB['PASSWORD']}@{DB['HOST']}/{DB['NAME']}"
    )
    MEDIA_ROOT = os.getenv("MEDIA_ROOT")
    CONTENT_TYPES = ['image/jpeg', 'image/png', 'image/gif']


class JWTSettings(BaseModel):
    authjwt_secret_key = os.getenv("SECRET_KEY")
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_csrf_protect: bool = False


@AuthJWT.load_config
def get_config():
    return JWTSettings()


SAFE_METHODS = ["GET", "HEAD", "OPTIONS", "TRACE"]

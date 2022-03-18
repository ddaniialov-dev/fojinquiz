import os

from dotenv import load_dotenv


load_dotenv()

DATABASE = {
    "USER": os.getenv("POSTGRES_USER"),
    "HOST": os.getenv("POSTGRES_HOST"),
    "NAME": os.getenv("POSTGRES_DB"),
    "PASSWORD": os.getenv("POSTGRES_PASSWORD")
}

DATABASE_URL = f"postgresql+asyncpg://{DATABASE['USER']}:{DATABASE['PASSWORD']}@{DATABASE['HOST']}/{DATABASE['NAME']}"
MEDIA_ROOT = os.getenv('MEDIA_ROOT')

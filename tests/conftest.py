import pytest
from fastapi import Depends
from fastapi.testclient import TestClient
from fastapi_jwt_auth import AuthJWT
from sqlalchemy import insert, update, create_engine, delete
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from main import app
from quiz_project.behaviours.base_model import AbstractBaseModel
from quiz_project.database import get_session
from quiz_project.utils.dependencies import get_current_user
from quiz_project.utils.functions import hash_password
from user_app.crud import UserManager
from user_app.models import User

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"


engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)


async def override_get_db():
    test_async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False)

    async with engine.begin() as connection:
        await connection.run_sync(AbstractBaseModel.metadata.create_all)

    async with test_async_session() as session:
        yield session

    # async with engine.begin() as connection:
    #     await connection.run_sync(AbstractBaseModel.metadata.drop_all)


app.dependency_overrides[get_session] = override_get_db


@pytest.fixture
def test_client():
    client = TestClient(app)
    yield client


@pytest.fixture
def registered_user(test_client):
    register_data = {
        'username': 'testuser',
        'email': 'test@fojin.tech',
        'password': 'Qwerty134'
    }
    test_client.post('/register/', json=register_data)
    yield test_client


@pytest.fixture
def auth_user():
    client = TestClient(app)
    login_data = {
        'username': 'testuser',
        'password': 'Qwerty134'
    }
    client.post('/login/', json=login_data)
    yield client


def create_admin():
    SQLALCHEMY_SYNC_DATABASE_URL = "sqlite:///./test.db"
    engine = create_engine(SQLALCHEMY_SYNC_DATABASE_URL, future=True)
    with engine.begin() as connection:
        password = hash_password(username='admin', password='Qwerty134')
        query = (
            insert(User).
            values(
                username='admin',
                hashed_password=password,
                email='admin@fojin.tech',
                is_admin=True
            )
        )
        connection.execute(query)


def drop_admin():
    SQLALCHEMY_SYNC_DATABASE_URL = "sqlite:///./test.db"
    engine = create_engine(SQLALCHEMY_SYNC_DATABASE_URL, future=True)
    with engine.begin() as connection:
        query = delete(User).where(User.username == 'admin')
        connection.execute(query)


@pytest.fixture
def auth_admin():
    client = TestClient(app)
    create_admin()
    admin_data = {
        'username': 'admin',
        'password': 'Qwerty134'
    }
    client.post('/login/', json=admin_data)
    yield client
    drop_admin()

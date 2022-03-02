import hashlib
from uuid import NAMESPACE_X500, uuid5

from sqlalchemy import and_
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User
from .schemas import UserCreate


class UserManager:
    
    def __init__(self, database: AsyncSession):
        self.db = database

    async def check_user_credentials(self, username: str, password: str):
        salt = uuid5(NAMESPACE_X500, username).hex.encode()
        hashed_password = hashlib.sha512(password.encode() + salt).hexdigest()
        query = select(User).where(
            and_(User.username == username, User.hashed_password == hashed_password)
        )
        response = await self.db.execute(query)
        return response.first()

    async def get_user(self, user_id: int):
        query = select(User).where(User.id == user_id)
        response = await self.db.execute(query)
        return response.first()

    async def get_user_by_username(self, username: str):
        query = select(User).where(User.username == username)
        response = await self.db.execute(query)
        return response.first()

    async def get_users(self, skip: int = 0, limit: int = 100):
        query = select(User).offset(skip).limit(limit)
        response = await self.db.execute(query)
        return response.all()

    async def create_user(self, user: UserCreate):
        salt = uuid5(NAMESPACE_X500, user.username).hex.encode()
        password = user.password.encode()
        hashed_password = hashlib.sha512(password + salt).hexdigest()
        db_user = User(username=user.username, hashed_password=hashed_password)

        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)

        return db_user
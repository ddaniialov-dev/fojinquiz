from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base

from .conf import DATABASE_URL


engine = create_async_engine(DATABASE_URL)
session_local = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession, expire_on_commit=False
)
Base = declarative_base()


async def get_database_session():
    session_instance = session_local()

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    async with session_instance as session:
        yield session

from sqlalchemy.ext.asyncio import AsyncSession


class AbstractBaseManager:
    def __init__(self, database: AsyncSession):
        self._database_session = database

    async def __aenter__(self):
        self._database_session.begin()

        return self

    async def __aexit__(self, exception_type, exception_value, exception_traceback):
        if not exception_type and not exception_traceback:
            await self._database_session.commit()
            await self._database_session.close()
        else:
            await self._database_session.rollback()

    async def create(self, obj):
        await self._before_create()

        self._database_session.add(obj)
        await self._database_session.commit()
        await self._database_session.refresh(obj)
        await self._after_create()

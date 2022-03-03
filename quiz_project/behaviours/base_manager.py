from abc import ABC

from sqlalchemy.ext.asyncio import AsyncSession

from .base_model import AbstractBaseModel


class AbstractBaseManager(ABC):
    
    def __init__(self, database: AsyncSession):
        self.__database_session = database

    async def __aenter__(self):
        self.__database_session.begin()

        return self.__database_session

    async def __aexit__(self, exception_type, exception_value, exception_traceback):
        match bool(exception_type):
            case False:
                self.__database_session.commit()
                self.__database_session.close()
            case True:
                self.__database_session.rollback()
                return True

    async def _before_create(self, *args, **kwargs):
        pass

    async def _after_create(self, *args, **kwargs):
        pass
    
    async def create(self, obj: AbstractBaseModel):
        await self._before_create()

        self.__database_session.add(self)
        await self.__database_session.refresh(obj)

        await self._after_create()

    async def _before_update(self, *args, **kwargs):
        pass

    async def _after_update(self, *args, **kwargs):
        pass

    async def update(self, *args, **kwargs):
        await self._before_update(*args, **kwargs)
        await self.__database_session.commit()
        await self._after_update(*args, **kwargs)

    async def delete(self, commit: bool = True):
        await self.__database_session.delete(self)

        if commit:
            await self.__database_session.commit()

from abc import ABC

from sqlalchemy.ext.asyncio import AsyncSession

from quiz_project import BaseModel


class AbstractBaseManager(ABC):
    
    def __init__(self, database: AsyncSession):
        self.__database_session = database

    def __aenter__(self):
        self.__database_session.begin()

        return self.__database_session

    def __aexit__(self, exception_type, exception_value, exception_traceback):
        match bool(exception_type):
            case False:
                self.__database_session.commit()
                await self.__database_session.close()
            case True:
                self.__database_session.rollback()
                return True

    async def _before_save(self, *args, **kwargs):
        pass

    async def _after_save(self, *args, **kwargs):
        pass

    async def __save(self):
        await self.__database_session.commit()
    
    async def create(self, obj: BaseModel, commit: bool = True):
        await self._before_save()

        self.__database_session.add(self)
        if commit:
            try:
                await self.__database_session.commit()
            except Exception as exception:
                await self.__database_session.rollback()
                raise exception

        await self.__database_session.refresh(obj)
        await self._after_save()

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

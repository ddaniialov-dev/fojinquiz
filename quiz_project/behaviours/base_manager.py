from abc import ABC
from typing_extensions import Self
from sqlalchemy.ext.asyncio import AsyncSession

from quiz_project.behaviours.base_model import BaseModel


class AbstractBaseManager(ABC):
    
    def __init__(self, database: AsyncSession):
        self.db = database
    
    async def before_save(self, *args, **kwargs):
        pass

    async def after_save(self, *args, **kwargs):
        pass
    
    async def save(self, obj, commit: bool = True):
        await self.before_save()
        self.db.add(self)
        if commit:
            try:
                await self.db.commit()
            except Exception as e:
                await self.db.rollback()
                raise e
        await self.db.refresh(obj)
        await self.after_save()


    async def before_update(self, *args, **kwargs):
        pass

    async def after_update(self, *args, **kwargs):
        pass

    async def update(self, *args, **kwargs):
        await self.before_update(*args, **kwargs)
        await self.db.commit()
        await self.after_update(*args, **kwargs)

    async def delete(self, commit: bool = True):
        await self.db.delete(self)
        if commit:
            await self.db.commit()
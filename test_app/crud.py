from sqlalchemy import delete, select, update
from sqlalchemy import and_
from quiz_project import AbstractBaseManager

from test_app.models import Test
from test_app.schemas import TestSchema


class TestManager(AbstractBaseManager):
    
    async def get_tests(self, holder):
        query = select(Test).where(Test.holder == holder.id)
        result = await self._database_session.execute(query)
        return result.all()
    
    async def get_user_tests(self, user_id: int) -> List[Test]:
        query = select(Test).where(Test.holder == user_id)
        result = await self._database_session.execute(query)
        return result.all()
    
    async def get_test(self, test_id: int):
        query = select(Test).where(Test.id == test_id)
        result = await self._database_session.execute(query)
        return result.first()

    async def create_test(self, test: TestSchema) -> int:
        test_object = Test(holder=test.holder, published=test.published)
        await self.create(test_object)
        return test_object.id

    async def delete_test(self, holder, test_id: int):
        query = delete(Test).where(
            and_(Test.id == test_id, holder.id == Test.holder)
            )
        return await self._database_session.execute(query)
    
    async def update_test(self, holder, test_id: int, data):
        query =  update(Test).returning(Test).where(
            and_(Test.id==test_id, Test.holder == holder.id)
            ).values(**data)
        result =  await self._database_session.execute(query)
        return result.first()
    

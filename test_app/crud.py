from sqlalchemy.future import select

from quiz_project.behaviours import AbstractBaseManager

from test_app.models import Test
from test_app.schemas import TestSchema


class TestManager(AbstractBaseManager):
    
    async def get_tests(self):
        query = select(Test)
        response = await self._database_session.execute(query)
        return response.all()
    
    async def get_user_tests(self, user_id: int):
        query = select(Test).where(Test.holder == user_id)
        response = await self._database_session.execute(query)
        return response.all()
    
    async def get_test(self, test_id: int):
        query = select(Test).where(Test.id == test_id)
        response = await self._database_session.execute(query)
        return response.first()

    async def create_test(self, test: TestSchema):
        test_object = Test(holder=test.holder, published=test.published)
        data = await self.create(test_object)
        return data.id

    async def delete_test(self, test_id: int):
        query = select(Test).where(Test.id == test_id).first()
        test_object = await self._database_session.execute(query)
        await self.delete(test_object)

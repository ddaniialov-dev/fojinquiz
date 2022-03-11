from typing import List

from sqlalchemy import delete, select

from quiz_project import AbstractBaseManager

from test_app.models import Test
from test_app.schemas import TestSchema


class TestManager(AbstractBaseManager):
    
    async def get_tests(self) -> List[Test]:
        query = select(Test)
        response = await self._database_session.execute(query)
        return response.all()
    
    async def get_user_tests(self, user_id: int) -> List[Test]:
        query = select(Test).where(Test.holder == user_id)
        response = await self._database_session.execute(query)
        return response.all()
    
    async def get_test(self, test_id: int) -> Test:
        query = select(Test).where(Test.id == test_id)
        response = await self._database_session.execute(query)
        return response.first()

    async def create_test(self, test: TestSchema) -> int:
        test_object = Test(holder=test.holder, published=test.published)
        await self.create(test_object)
        return test_object.id

    async def delete_test(self, test_id: int) -> None:
        query = delete(Test).where(Test.id == test_id)
        await self._database_session.execute(query)

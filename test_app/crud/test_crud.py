from typing import List

from sqlalchemy import delete, select, update, and_

from user_app.models import User
from test_app.models import Test
from test_app.schemas import CreateTest
from quiz_project.behaviours import AbstractBaseManager


class TestManager(AbstractBaseManager):

    async def get_tests(self) -> List[Test]:
        query = select(Test)
        result = await self._database_session.execute(query)
        return [result[0] for result in result.all()]

    async def get_user_tests(self, user_id: int) -> List[Test]:
        query = (
            select(Test)
            .where(Test.holder == user_id)
        )

        result = await self._database_session.execute(query)
        return [result[0] for result in result.all()]

    async def get_test(self, test_id: int) -> Test:
        query = (
            select(Test)
            .where(Test.id == test_id)
        )

        result = await self._database_session.execute(query)
        return result.first()

    async def create_test(self, test: CreateTest) -> Test:
        test_object = Test(holder=test.holder, published=test.published)
        await self.create(test_object)
        return test_object

    async def delete_test(self, holder: User, test_id: int) -> Test:
        query = (
            delete(Test)
            .returning(Test)
            .where(and_(Test.id == test_id, holder.id == Test.holder))
        )

        result = await self._database_session.execute(query)
        return result.first()

    async def update_test(self, holder: User, test_id: int, data: dict) -> Test:
        query = (
            update(Test)
            .returning(Test)
            .where(and_(Test.id == test_id, Test.holder == holder.id))
            .values(**data)
        )

        result = await self._database_session.execute(query)
        return result.first()[0]

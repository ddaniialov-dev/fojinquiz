from typing import List

from sqlalchemy import delete, select, update, and_
from sqlalchemy.orm import selectinload

from user_app.models import User
from test_app.models import Test
from test_app.schemas import CreateTest
from quiz_project.behaviours.base_manager import AbstractBaseManager


class TestManager(AbstractBaseManager):

    async def get_tests(self) -> List[Test]:
        query = select(Test)
        result = await self._database_session.execute(query)
        return result.scalars().fetchall()

    async def get_user_tests(self, user_id: int) -> List[Test]:
        query = (
            select(Test)
            .where(Test.holder_id == user_id)
        )

        result = await self._database_session.execute(query)
        return result.scalars().fetchall()

    async def get_test(self, test_id: int) -> Test:
        query = (
            select(Test)
            .options(selectinload(Test.questions))
            .where(Test.id == test_id)
        )

        result = await self._database_session.execute(query)
        return result.scalars().one_or_none()

    async def create_test(self, test: CreateTest) -> Test:
        test_object = Test(**test.dict())
        await self.create(test_object)
        return test_object

    async def delete_test(self, holder: User, test_id: int) -> Test:
        query = (
            delete(Test)
            .returning(Test)
            .where(and_(Test.id == test_id, holder.id == Test.holder_id))
        )

        result = await self._database_session.execute(query)
        return result.scalars()

    async def update_test(self, test_id: int, data: dict) -> Test:
        query = (
            update(Test)
            .returning(Test)
            .where(and_(Test.id == test_id))
            .values(**data)
        )

        result = await self._database_session.execute(query)
        return result.first()

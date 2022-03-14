from sqlalchemy import delete, select, update

from quiz_project import AbstractBaseManager

from test_app.models import Test
from test_app.schemas import TestSchema


class TestManager(AbstractBaseManager):
    
    async def get_tests(self, holder):
        query = select(Test).where(Test.holder == holder.id)
        result = await self._database_session.execute(query)
        return result.all()
    
    async def get_user_tests(self, user_id: int):
        query = select(Test).where(Test.holder == user_id)
        result = await self._database_session.execute(query)
        return result.all()
    
    async def get_test(self, holder, test_id: int):
        query = select(Test).where(
            Test.id == test_id and holder.id == Test.holder
            )
        result = await self._database_session.execute(query)
        result = result.first()

    async def create_test(self, test: TestSchema):
        test_object = Test(holder=test.holder, published=test.published)
        await self.create(test_object)
        return test_object.id

    async def delete_test(self, holder, test_id: int):
        query = delete(Test).where(
            Test.id == test_id and holder.id == Test.holder
            )

        return await self._database_session.execute(query)
    
    async def update_test(self, holder, test_id: int, data):
        query =  update(Test).where(
            Test.id==test_id and holder.id == Test.holder
            ).values(**data)

        return self._database_session.execute(query)
from select import select
from quiz_project.behaviours import AbstractBaseManager
from test_app.models import Test
from test_app.schemas import TestSchema

class TestManager(AbstractBaseManager):
    
    async def get_tests(self):
        query = select(Test)
        response = await self.db.execute(query)
        response
    
    async def get_user_tests(self, user_id: int):
        query = select(Test).where(Test.user.id == user_id)
        response = await self.db.execute(query)
        return response
    
    async def get_test(self, test_id: int):
        query = select(Test).where(Test.id == test_id)
        response = await self.db.execute(query)
        return response

    async def create_test(self, test: TestSchema):
        db_test = Test(holder=test.holder, published=test.published)
        await self.save(db_test)

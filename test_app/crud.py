from typing import List

from sqlalchemy import delete, select

from quiz_project import AbstractBaseManager

from test_app.models import Test, Image
from test_app.schemas import TestSchema, ImageSchema


class TestManager(AbstractBaseManager):
    
    async def get_tests(self) -> List[Test]:
        query = select(Test)
        response = await self._database_session.execute(query)
        return [test[0] for test in response.all()]
    
    async def get_user_tests(self, user_id: int) -> List[Test]:
        query = select(Test).where(Test.holder == user_id)
        response = await self._database_session.execute(query)
        return [test[0] for test in response.all()]
    
    async def get_test(self, test_id: int) -> Test:
        query = select(Test).where(Test.id == test_id)
        response = await self._database_session.execute(query)
        return response[0]

    async def create_test(self, test: TestSchema) -> int:
        test_object = Test(holder=test.holder, published=test.published)
        await self.create(test_object)
        return test_object.id

    async def delete_test(self, test_id: int) -> None:
        query = delete(Test).where(Test.id == test_id)
        await self._database_session.execute(query)


class QuestionManager(AbstractBaseManager):

    async def get_questions(self, question):
        pass

    async def create_image(self, image: ImageSchema) -> int:
        image_object = Image(**image.dict())
        await self.create(image_object)
        return image_object.id

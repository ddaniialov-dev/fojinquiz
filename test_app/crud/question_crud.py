from typing import List

from sqlalchemy import select, update, and_, delete

from schemas import CreateQuestion, UpdateQuestion
from test_app.models import Image, Question, Test
from test_app.schemas import ImageSchema
from quiz_project import AbstractBaseManager
from user_app import User


class QuestionManager(AbstractBaseManager):

    async def get_questions(self) -> List[Question]:
        query = select(Question)
        response = await self._database_session.execute(query)
        return [result[0] for result in response.all()]

    async def get_question(self, question_id: int) -> Question:
        query = (
            select(Question)
            .where(Question.id == question_id)
        )
        response = await self._database_session.execute(query)
        return response.first()

    async def create_question(self, holder: User, question: CreateQuestion) -> Question:
        query = (
            select(Test)
            .where(and_(
                Test.id == question.test, Test.holder == holder.id
            ))
        )
        response = await self._database_session.execute(query)
        test = response.first()

        if test:
            question_object = Question(text=question.text, test=question.test)
            await self.create(question_object)
            return question_object

    async def update_question(self, holder: User, question: UpdateQuestion) -> Question:
        query = (
            select(Test)
            .where(and_(
                Test.id == question.test, Test.holder == holder.id
            ))
        )
        response = await self._database_session.execute(query)
        test = response.first()
        query = (
            update(Question)
            .returning(Question)
            .where(Question.test == test.id)
            .values()
        )
        response = await self._database_session.execute(query)
        return response.first()

    async def delete_question(self, holder: User, question_id: int) -> None:
        question = await self.get_question(question_id)
        query = (
            select(Test)
            .where(and_(
                Test.id == question.test, Test.holder == holder.id
            ))
        )
        response = await self._database_session.execute(query)
        test = response.first()

        if not test:
            return None

        query = (
            delete(Question)
            .returning(Question)
            .where(Question.id == question_id)
        )
        response = await self._database_session.execute(query)
        return response.first()[0]

    async def get_image(self, question_id: int) -> Image:
        query = (
            select(Image)
            .where(Image.question == question_id)
        )
        response = await self._database_session.execute(query)
        return response.first()[0]

    async def create_image(self, image: ImageSchema) -> int:
        image_object = Image(**image.dict())
        await self.create(image_object)
        return image_object.id

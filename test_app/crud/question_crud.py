import os

from sqlalchemy import select, update, delete, and_
from sqlalchemy.orm import selectinload

from test_app.schemas import CreateQuestion
from test_app.models import Image, Question, Test
from test_app.schemas import ImageSchema
from quiz_project.behaviours.base_manager import AbstractBaseManager
from quiz_project.conf import Settings


class QuestionManager(AbstractBaseManager):
    async def get_test(self, test_id: int) -> Test:
        query = (
            select(Test).options(selectinload(
                Test.questions)).where(Test.id == test_id)
        )

        result = await self._database_session.execute(query)
        return result.scalars().one_or_none()

    async def get_questions(self, test_id) -> list[Question]:
        query = select(Question).where(Question.test_id == test_id)
        result = await self._database_session.execute(query)
        return result.scalars().fetchall()

    async def get_question(self, question_id: int) -> Question:
        query = select(Question).where(Question.id == question_id)
        result = await self._database_session.execute(query)
        return result.scalars().one_or_none()

    async def create_question(self, question: CreateQuestion, test: Test) -> Question:
        question_object = Question(
            **question.dict(), test_id=test.id, ordering=len(test.questions) + 1
        )
        await self.create(question_object)
        return question_object

    async def change_ordering(self, data: dict, question_id: int) -> None:
        query = select(Question).where(Question.id == question_id)
        result = await self._database_session.execute(query)
        question = result.scalar()
        ordering = data.get("ordering")
        if ordering > question.ordering:
            await self._database_session.execute(
                update(Question)
                .where(
                    and_(
                        Question.ordering <= ordering,
                        Question.ordering > question.ordering,
                    )
                )
                .values(ordering=Question.ordering - 1)
            )
        elif ordering < question.ordering:
            await self._database_session.execute(
                update(Question)
                .where(
                    and_(
                        Question.ordering >= ordering,
                        Question.ordering < question.ordering,
                    )
                )
                .values(ordering=Question.ordering + 1)
            )

    async def update_question(self, data: dict, question_id: int) -> Question:
        if data.get("ordering"):
            await self.change_ordering(data, question_id)
        query = (
            update(Question)
            .returning(Question)
            .where(Question.id == question_id)
            .values(data)
        )
        response = await self._database_session.execute(query)
        return response.first()

    async def delete_question(self, question_id: int) -> None:

        query = delete(Question).returning(
            Question).where(Question.id == question_id)
        result = await self._database_session.execute(query)
        query = (
            update(Question)
            .where(Question.ordering > result.first().ordering)
            .values(ordering=Question.ordering - 1)
        )
        await self._database_session.execute(query)

    async def get_image(self, question_id: int) -> Image:
        query = select(Image).where(Image.question == question_id)
        response = await self._database_session.execute(query)
        return response.scalars().first()

    async def create_image(self, image: ImageSchema) -> int:
        image_object = Image(**image.dict())
        await self.create(image_object)
        return image_object.id

    async def delete_images(self, question_id: int) -> None:
        query = delete(Image).returning(Image).where(
            Image.question == question_id)
        result = await self._database_session.execute(query)
        images = result.all()
        for image in images:
            os.remove(Settings.MEDIA_ROOT + image.path)

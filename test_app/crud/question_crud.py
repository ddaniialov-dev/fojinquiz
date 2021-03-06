from typing import List

from sqlalchemy import select, update, and_, delete
from sqlalchemy.orm import selectinload

from test_app.schemas import CreateQuestion, UpdateQuestion
from test_app.models import Image, Question, Test
from test_app.schemas import ImageSchema
from quiz_project.behaviours.base_manager import AbstractBaseManager
from user_app.models import User


class QuestionManager(AbstractBaseManager):
    async def get_test(self, test_id: int) -> Test:
        query = (
            select(Test).options(selectinload(Test.questions)).where(Test.id == test_id)
        )

        result = await self._database_session.execute(query)
        return result.scalars().one_or_none()

    async def get_questions(self, test_id) -> List[Question]:
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

    async def update_question(self, data: dict, question_id: int) -> Question:
        ordering = data.get("ordering")
        if ordering:
            query = select(Question)
            result = await self._database_session.execute(query)
            questions = result.scalars().fetchall()
            question_object = list(filter(lambda x: x.id == question_id, questions))[0]
            if ordering > question_object.ordering:
                for question in questions:
                    if question.ordering in range(
                        question_object.ordering + 1, ordering + 1
                    ):
                        question.ordering -= 1
                question_object.ordering = ordering
            elif ordering < question_object.ordering:
                for question in questions:
                    if question.ordering in range(
                        ordering, question_object.ordering + 1
                    ):
                        question.ordering += 1
                question_object.ordering = ordering
            self._database_session.commit()
            data.pop("ordering")

        query = (
            update(Question)
            .returning(Question)
            .where(Question.id == question_id)
            .values(data)
        )
        response = await self._database_session.execute(query)
        return response.first()

    async def delete_question(self, question_id: int) -> None:
        query = delete(Question).returning(Question).where(Question.id == question_id)
        await self._database_session.execute(query)

    async def get_image(self, question_id: int) -> Image:
        query = select(Image).where(Image.question == question_id)
        response = await self._database_session.execute(query)
        return response.scalars().one_or_none()

    async def create_image(self, image: ImageSchema) -> int:
        image_object = Image(**image.dict())
        await self.create(image_object)
        return image_object.id

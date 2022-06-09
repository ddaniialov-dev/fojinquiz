from sqlalchemy import delete, select, update, and_

from quiz_project.behaviours.base_manager import AbstractBaseManager
from test_app.models import Answer, Question
from test_app.schemas.answer_scheme import CreateAnswer


class AnswerManager(AbstractBaseManager):
    async def get_question(self, question_id):
        query = select(Question).where(Question.id == question_id)
        result = await self._database_session.execute(query)
        question = result.scalar()
        return question

    async def create_answer(
        self, answer: CreateAnswer, question_id: int
    ) -> Answer | None:
        answer_object = Answer(question_id=question_id, **answer.dict())
        query = select(Answer).where(
            and_(Answer.question_id == question_id, Answer.is_true)
        )
        result = await self._database_session.execute(query)
        if result.scalar() and answer.is_true:
            return None
        await self.create(answer_object)
        return answer_object

    async def get_answers(self, question_id) -> list[Answer]:
        query = (
            select(Answer).where(Answer.question_id ==
                                 question_id).order_by(Answer.id)
        )
        result = await self._database_session.execute(query)
        return result.scalars().fetchall()

    async def get_answer(self, answer_id) -> Answer:
        query = select(Answer).where(Answer.id == answer_id)
        result = await self._database_session.execute(query)
        return result.scalars().one_or_none()

    async def update_answer(self, answer_id: int, data: dict, question_id: int) -> Answer:
        if data.get("is_true"):
            query = update(Answer).where(Answer.question_id == question_id).values({"is_true": False})
            response = await self._database_session.execute(query)
        query = (
            update(Answer).returning(Answer).where(
                Answer.id == answer_id).values(data)
        )

        response = await self._database_session.execute(query)
        return response.first()

    async def delete_answer(self, answer_id: int) -> None:
        query = delete(Answer).returning(Answer).where(Answer.id == answer_id)
        await self._database_session.execute(query)

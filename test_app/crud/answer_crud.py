from sqlalchemy import delete, select, update, and_
from sqlalchemy.orm import joinedload

from quiz_project.behaviours.base_manager import AbstractBaseManager
from test_app.models import Answer, Question, Test
from test_app.schemas.answer_scheme import CreateAnswer


class AnswerManager(AbstractBaseManager):

    async def get_question(self, question_id):
        query = (
            select(Question)
            .where(Question.id == question_id)
        )
        result = await self._database_session.execute(query)
        question = result.scalar()
        return question

    async def create_answer(self, answer: CreateAnswer, question_id: int) -> Answer:
        answer_object = Answer(question_id=question_id, **answer.dict())
        await self.create(answer_object)
        return answer_object
    
    async def get_answers(self, question_id) -> list[Answer]:
        query =  (
            select(Answer)
            .where(Answer.question_id == question_id)
        )
        result = await self._database_session.execute(query)
        return result.scalars().fetchall()
    
    async def get_answer(self, answer_id) -> Answer:
        query =  (
            select(Answer)
            .where(Answer.id == answer_id)
        )
        result = await self._database_session.execute(query)
        return result.scalars().one_or_none()
    
    async def update_answer(self, answer_id: int, data: dict) -> Answer:
        query = (
            update(Answer)
            .returning(Answer)
            .where(Answer.id == answer_id)
            .values(data)
        )
        response = await self._database_session.execute(query)
        return response.first()
    
    async def delete_answer(self, answer_id: int) -> None:
        query = (
            delete(Answer)
            .returning(Answer)
            .where(Answer.id == answer_id)
        )
        await self._database_session.execute(query)

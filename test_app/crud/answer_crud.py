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

    async def create_answer(self, user, question_id: int, answer: CreateAnswer):
        answer_object = Answer(question_id=question_id, **answer.dict())
        await self.create(answer_object)
        return answer_object
    
    async def get_answers(self, question_id):
        query =  (
            select(Answer)
            .where(Answer.question_id == question_id)
        )
        result = await self._database_session.execute(query)
        answer_objects = result.scalars().fetchall()
        return answer_objects

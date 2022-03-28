from sqlalchemy import delete, select, update, and_
from sqlalchemy.orm import selectinload

from quiz_project.behaviours.base_manager import AbstractBaseManager
from test_app.models import Answer, Question, Test
from test_app.schemas.answer_scheme import CreateAnswer


class AnswerManager(AbstractBaseManager):
    async def create_answer(self, auth, answer: CreateAnswer):
        query = (
            select(Question)
            .where(Question.id == answer.question)
        )
        result = await self._database_session.execute(query)
        question = result.scalar()
        test_query = (
            select(Test)
            .where(question.test == auth.id)
        )
        result = await self._database_session.execute(test_query)
        if not result.all():
            return None
        answer_object = Answer(**answer.dict())
        await self.create(answer_object)
        return answer_object
    
    async def get_answers(self, question_id):
        

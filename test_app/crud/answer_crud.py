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

    async def create_answer(self, user, question_id: id, answer: CreateAnswer):
        question = await self.get_question(question_id)

        if question.test.holder != user.id or not question:
            return None
            
        answer_object = Answer(**answer.dict())
        await self.create(answer_object)
        return answer_object
    
    async def get_answers(self, question_id):
        pass

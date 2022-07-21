from sqlalchemy import and_, select

from quiz_project.behaviours.base_manager import AbstractBaseManager
from test_app.checks.user_answers import check_if_not_question
from test_app.models import Answer, Session, UserAnswer
from user_app.models import User


class UserAnswerManager(AbstractBaseManager):
    async def create_user_answer(
            self,
            session: Session,
            data: dict,
            user: User
    ) -> UserAnswer:
        query = (
            select(Answer).where(Answer.id == data["answer_id"])
        )
        result = await self._database_session.execute(query)
        answer = result.scalar()
        user_answer = UserAnswer(
            session_id=session.id,
            **data, user_id=user.id,
            question_id=answer.question_id
        )
        await check_if_not_question(session, answer.question)

        await self.create(user_answer)
        session.questions.remove(user_answer.question)
        return user_answer

    async def get_user_answer(self, session_id: int, user: User):
        query = (
            select(UserAnswer).where(
                and_(UserAnswer.session_id == session_id,
                     UserAnswer.user_id == user.id)
            )
        )
        result = await self._database_session.execute(query)
        return result.scalars().fetchall()

    async def get_right_answer(self, question_id: int):
        query = (
            select(Answer).where(and_(
                Answer.question_id == question_id,
                Answer.is_true
            ))
        )
        result = await self._database_session.execute(query)
        return result.scalar()

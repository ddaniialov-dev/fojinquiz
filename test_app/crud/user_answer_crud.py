from sqlalchemy import select

from quiz_project.behaviours.base_manager import AbstractBaseManager
from test_app.models import UserAnswer


class UserAnswerManager(AbstractBaseManager):
    async def get_user_answers(self, session_id: int) -> list[UserAnswer]:
        query = (
            select(UserAnswer)
            .where(UserAnswer.session_id == session_id)
        )
        
        result = await self._database_session.execute(query)
        return result.scalars().fetchall()
    
    async def create_user_answer(self, data: dict) -> UserAnswer:
        user_answer = UserAnswer(**data)
        await self.create(user_answer)
        return user_answer

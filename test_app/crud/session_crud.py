import re
from typing import List

from sqlalchemy import delete, select, and_
from sqlalchemy.orm import joinedload

from quiz_project.behaviours.base_manager import AbstractBaseManager
from quiz_project.database import get_session
from test_app.models import Session, Test
from user_app.models import User


class SessionManager(AbstractBaseManager):

    async def get_test(self, test_id: int) -> Test:
        query = (
            select(Test)
            .where(Test.id == test_id)
        )

        result = await self._database_session.execute(query)
        return result.scalars().one_or_none()

    async def get_sessions(self, user_id: int) -> List[Session]:
        query = (
            select(Session)
            .where(Session.user_id == user_id)
        )
        result = await self._database_session.execute(query)
        return [result[0] for result in result.all()]

    async def get_session(self, user_id: int, session_id: int) -> Session:
        query = (
            select(Session)
            .options(joinedload(Session.questions))
            .where(and_(Session.id == session_id, Session.user_id == user_id))
        )

        result = await self._database_session.execute(query)
        return result.scalar()

    async def create_session(self, test_id: int, user: User):
        query = (
            select(Test)
            .where(Test.id == test_id)
            .options(joinedload(Test.questions))
        )
        result = await self._database_session.execute(query)
        test = result.scalar()

        session_object = Session(test_id=test.id, user_id=user.id, questions=test.questions)
        await self.create(session_object)
        session_object = await self.get_session(user.id, session_object.id)
        return session_object

    async def delete_session(self, session_id: int):
        query = (
            delete(Session).
            returning(Session)
            .where(
                and_(Session.id == session_id)
            )
        )

        result = await self._database_session.execute(query)
        return result.first()

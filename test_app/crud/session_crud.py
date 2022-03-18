import re
from typing import List

from sqlalchemy import delete, select, update, and_

from quiz_project import AbstractBaseManager
from test_app.models import Session, Test
from test_app.schemas import CreateSession
from user_app.models import User


class SessionManager(AbstractBaseManager):
    async def get_sessions(self, user_id: int) -> List[Session]:
        query = (
            select(Session)
            .where(Session.user == user_id)
        )
        result = await self._database_session.execute(query)
        return [result[0] for result in result.all()]

    async def get_session(self, user_id: int, session_id: int) -> Session:
        query = (
            select(Session)
            .where(and_(Session.id == session_id, Session.user == user_id))
        )

        result = await self._database_session.execute(query)
        return result.first()[0]

    async def create_session(self, user, session: CreateSession):
        query = (
            select(Test)
            .where(Test.id == session.test)
        )
        result = await self._database_session.execute(query)
        test = result.first()
        session.questions = test.questions.all()

        session_object = Session(**session.dict())
        await self.create(session_object)
        return session_object

    async def delete_session(self, user: User, session_id: int):
        query = (
            delete(Session).
            returning(Session)
            .where(
                and_(Session.id == session_id, Session.user == user.id)
            )
        )

        result = await self._database_session.execute(query)
        return result.first()

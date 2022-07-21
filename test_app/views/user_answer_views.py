from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from quiz_project.database import get_session
from quiz_project.utils.dependencies import get_current_user
from test_app.checks.common import check_if_exists
from test_app.crud.session_crud import SessionManager
from test_app.crud.user_answer_crud import UserAnswerManager
from test_app.schemas.user_answer_schemas import (CreateUserAnswer,
                                                  GetUserAnswer,
                                                  GetUserAnswers)
from user_app.models import User

user_answer_router = APIRouter(
    prefix="/sessions/{session_id}/user_answers",
    tags=["user_answers"],
)


@user_answer_router.post(
    "/",
    status_code=201,
    response_model=GetUserAnswer,
)
async def create_user_answer(
    session_id: int,
    user_answer: CreateUserAnswer,
    auth: User = Depends(get_current_user),
    database_session: AsyncSession = Depends(get_session),
):
    async with SessionManager(database_session) as manager:
        session_object = await manager.get_session(auth.id, session_id)
        await check_if_exists(session_object)
        if len(session_object.questions) == 1:
            await manager.set_finished_date(session_object.id)
        async with UserAnswerManager(database_session) as answer_manager:
            user_answer_object = await answer_manager.create_user_answer(
                session_object, user_answer.dict(), auth
            )
            return user_answer_object


@user_answer_router.get("/", response_model=List[GetUserAnswers])
async def get_user_answers(
        session_id: int,
        auth: User = Depends(get_current_user),
        database_session: AsyncSession = Depends(get_session)
):
    async with SessionManager(database_session) as manager:
        session_object = await manager.get_session(auth.id, session_id)
        await check_if_exists(session_object)
        async with UserAnswerManager(database_session) as answer_manager:
            user_answers = await answer_manager.get_user_answer(
                session_id=session_id, user=auth
            )
            array = []
            for element in user_answers:
                right_answer = await answer_manager.get_right_answer(
                    element.question_id
                )
                array.append(GetUserAnswers(
                    right_answer=right_answer,
                    **element.__dict__
                ))
            return array

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, Response
from test_app.checks.common import check_if_exists, check_if_exist, check_if_holder
from test_app.checks.answers import check_if_question_has_answer

from test_app.crud.answer_crud import AnswerManager
from test_app.schemas.answer_scheme import GetAnswer, CreateAnswer, UpdateAnswer

from quiz_project.database import get_session
from quiz_project.utils.dependencies import get_current_user
from user_app.models import User


answer_router = APIRouter(
    prefix="/questions/{question_id}",
    tags=["answers"],
)


@answer_router.post("/answers/", status_code=201, response_model=GetAnswer)
async def create_answer(
    question_id: int,
    answer: CreateAnswer,
    auth: User = Depends(get_current_user),
    database_session: AsyncSession = Depends(get_session),
):
    async with AnswerManager(database_session) as manager:
        question_object = await manager.get_question(question_id)
        await check_if_exists(question_object)
        await check_if_holder(auth.id, question_object.test.holder_id)
        answer_object = await manager.create_answer(answer, question_id)
        return answer_object


@answer_router.get("/answers/", status_code=200, response_model=list[GetAnswer])
async def get_answers(
    question_id: int,
    auth: User = Depends(get_current_user),
    database_session: AsyncSession = Depends(get_session),
):
    async with AnswerManager(database_session) as manager:
        question_object = await manager.get_question(question_id)
        await check_if_exists(question_object)
        await check_if_holder(auth.id, question_object.test.holder_id)
        answer_objects = await manager.get_answers(question_id)
        return answer_objects


@answer_router.get("/answers/{answer_id}/", status_code=200, response_model=GetAnswer)
async def get_answer(
    question_id: int,
    answer_id: int,
    auth: User = Depends(get_current_user),
    database_session: AsyncSession = Depends(get_session),
):
    async with AnswerManager(database_session) as manager:
        question_object = await manager.get_question(question_id)
        await check_if_exists(question_object)
        await check_if_holder(auth.id, question_object.test.holder_id)
        answer_object = await manager.get_answer(answer_id)
        await check_if_exists(answer_object)
        await check_if_question_has_answer(question_id, answer_object)
        return answer_object


@answer_router.put("/answers/{answer_id}/", status_code=200, response_model=GetAnswer)
async def update_answer(
    question_id: int,
    answer_id: int,
    answer: UpdateAnswer,
    auth: User = Depends(get_current_user),
    database_session: AsyncSession = Depends(get_session),
):
    async with AnswerManager(database_session) as manager:
        await get_answer(question_id, answer_id, auth, database_session)
        answer_object = await manager.update_answer(
            answer_id, answer.dict(exclude_unset=True)
        )
        return answer_object


@answer_router.delete(
    "/answers/{answer_id}/",
    status_code=200,
)
async def delete_answer(
    question_id: int,
    answer_id: int,
    auth: User = Depends(get_current_user),
    database_session: AsyncSession = Depends(get_session),
):
    async with AnswerManager(database_session) as manager:
        await get_answer(question_id, answer_id, auth, database_session)
        answer_object = await manager.delete_answer(answer_id)
        return Response(status_code=204)

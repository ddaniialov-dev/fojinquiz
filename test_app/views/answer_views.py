from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Response
from starlette.responses import StreamingResponse

from test_app.crud.answer_crud import AnswerManager
from test_app.schemas.answer_scheme import GetAnswer, CreateAnswer

from quiz_project.conf import Settings
from quiz_project.database import get_session
from quiz_project.utils.functions import save_file, get_file
from quiz_project.utils.dependencies import get_current_user
from user_app.models import User


answer_router = APIRouter(
    prefix='/questions/{question_id}',
    tags=['answers'],
)


@answer_router.post(
    '/',
    status_code=201,
    response_model=GetAnswer
)
async def create_answer(
    question_id: int,
    answer: CreateAnswer,
    auth: User = Depends(get_current_user),
    database_session: AsyncSession = Depends(get_session)
):
    async with AnswerManager(database_session) as answer_manager:
        answer_object = await answer_manager.create_answer(auth, question_id, answer)
        if not answer_object:
            raise HTTPException(
                status_code=404, detail='Permission denied'
            )

    return answer_object


@answer_router.get(
    '/answers/',
    status_code=200,
    response_model=List[GetAnswer] 
)
async def get_answers(
    question_id: int,
    auth: User = Depends(get_current_user),
    database_session: AsyncSession = Depends(get_session)
):
    async with AnswerManager(database_session) as answer_manager:
        answer_objects = await answer_manager.get_answers(auth, question_id)

        if not answer_objects:
            raise HTTPException(
                status_code=404, detail='data not found'
            )
    return answer_objects


@answer_router.get(
    '/answers/{answer_id}',
    status_code=200,
    response_model=GetAnswer
)
async def get_answers(
    question_id: int,
    auth: User = Depends(get_current_user),
    database_session: AsyncSession = Depends(get_session)
):
    async with AnswerManager(database_session) as answer_manager:
        answer_object = await answer_manager.get_answers(auth, question_id)

        if not answer_object:
            raise HTTPException(
                status_code=404, detail='data not found'
            )
    return answer_object

@answer_router.get(
    '/answers/{answer_id}/',
    status_code=200,
    response_model=GetAnswer
)
async def get_answer(
    question_id: int,
    auth: User = Depends(get_current_user),
    database_session: AsyncSession = Depends(get_session)
):
    async with AnswerManager(database_session) as answer_manager:
        answer_object = await answer_manager.get_answers(auth, question_id)

        if not answer_object:
            raise HTTPException(
                status_code=404, detail='data not found'
            )
    return answer_object


@answer_router.put(
    '/answers/{answer_id}/',
    status_code=200,
    response_model=GetAnswer
)
async def update_answer(
    question_id: int,
    answer_id: int,
    auth: User = Depends(get_current_user),
    database_session: AsyncSession = Depends(get_session)
):
    async with AnswerManager(database_session) as answer_manager:
        answer_object = await answer_manager.update_answer(auth, question_id, answer_id)

        if not answer_object:
            raise HTTPException(
                status_code=404, detail='data not found'
            )

    return answer_object


@answer_router.delete(
    '/answers/{answer_id}/',
    status_code=200,
)
async def delete_answer(
    question_id: int,
    answer_id: int,
    auth: User = Depends(get_current_user),
    database_session: AsyncSession = Depends(get_session)
):
    async with AnswerManager(database_session) as answer_manager:
        answer_object = await answer_manager.delete_answer(auth, question_id, answer_id)

        if not answer_object:
            raise HTTPException(
                status_code=404, detail='data not found'
            )

    return Response(status_code=204)

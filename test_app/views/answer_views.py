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
    prefix='/answers',
    tags=['answers'],
)


@answer_router.post(
    '/',
    status_code=201,
    response_model=GetAnswer
)
async def create_answer(
    answer: CreateAnswer,
    auth: User = Depends(get_current_user),
    database_session: AsyncSession = Depends(get_session)
):
    async with AnswerManager(database_session) as answer_manager:
        answer_object = await answer_manager.create_answer(auth, answer)

    return answer_object

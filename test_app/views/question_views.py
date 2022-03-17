from typing import List

from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File

from crud import QuestionManager
from models import Question
from quiz_project import (
    JwtAccessRequired,
    get_session,
    token_header,
    save_file,
    MEDIA_ROOT
)


question_router = APIRouter(
    prefix='/questions',
    tags=['questions'],
    dependencies=[Depends(token_header)]
)


@question_router.post(
    '/questions/',
    status_code=200,
    response_model=List[Question]
)
@JwtAccessRequired()
async def get_questions(
    auth: AuthJWT = Depends(),
    database_session: AsyncSession = Depends(get_session)
):
    async with QuestionManager(database_session) as question_manager:
                


@question_router.post(
    '/questions/'
)
@JwtAccessRequired()
async def get_questions():
    pass


@question_router.post(
    '{question_id}/attach_image/'
)
@JwtAccessRequired()
async def save_image(
        question_id: int,
        auth: AuthJWT = Depends(),
        files: List[UploadFile] = File(...),
        database_session: AsyncSession = Depends(get_session)
):
    for file in files:
        byte_data = await file.read()

        async with QuestionManager(database_session) as question_manager:
            save_file(MEDIA_ROOT + file.filename, byte_data)
            image_structure = {
                'path': file.filename,
                'content_type': file.content_type,
                'question': question_id
            }
            question_manager.create_image(image_structure)

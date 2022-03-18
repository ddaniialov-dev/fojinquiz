from typing import List

from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File

from test_app.crud import QuestionManager
from quiz_project import (
    get_session,
    save_file,
    MEDIA_ROOT
)


question_router = APIRouter(
    prefix='/questions',
    tags=['questions'],
)


@question_router.post(
    '/questions/'
)
async def get_questions():
    pass


@question_router.post(
    '{question_id}/attach_image/'
)
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

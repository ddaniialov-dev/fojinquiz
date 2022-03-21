import io
from typing import List

from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Response
from starlette.responses import StreamingResponse

from crud import QuestionManager
from schemas import UpdateQuestion, CreateQuestion, GetQuestion, ImageSchema

from quiz_project import (
    get_session,
    save_file,
    MEDIA_ROOT, get_current_user, get_file
)
from user_app.models import User


question_router = APIRouter(
    prefix='/questions',
    tags=['questions'],
)


@question_router.get(
    '/',
    status_code=200,
    response_model=List[GetQuestion]
)
async def get_questions(
    user: User = Depends(get_current_user),
    database_session: AsyncSession = Depends(get_session),
) -> List[GetQuestion]:
    async with QuestionManager(database_session) as question_manager:
        questions = await question_manager.get_questions()

    if not questions:
        raise HTTPException(
            status_code=404, detail='data not found'
        )

    return questions


@question_router.post(
    '/',
    status_code=201,
    response_model=GetQuestion
)
async def create_question(
    question: CreateQuestion,
    user: User = Depends(get_current_user),
    database_session: AsyncSession = Depends(get_session)
) -> GetQuestion:
    async with QuestionManager(database_session) as question_manager:
        question_object = await question_manager.create_question(user, question)


    return question_object


@question_router.get(
    '/{question_id}/',
    status_code=200,
    response_model=GetQuestion
)
async def get_question(
    question_id: int,
    user: User = Depends(get_current_user),
    database_session: AsyncSession = Depends(get_session)
) -> GetQuestion:
    async with QuestionManager(database_session) as question_manager:
        question = await question_manager.get_question(question_id)

    return question


@question_router.put(
    '/{question_id}/',
    status_code=200,
    response_model=GetQuestion
)
async def update_question(
    question: UpdateQuestion,
    user: User = Depends(get_current_user),
    database_session: AsyncSession = Depends(get_session)
) -> GetQuestion:
    async with QuestionManager(database_session) as question_manager:
        question = await question_manager.update_question(user, question)

    return question


@question_router.delete(
    '/{question_id}/',
    status_code=204,
)
async def delete_question(
    question: UpdateQuestion,
    user: User = Depends(get_current_user),
    database_session: AsyncSession = Depends(get_session)
) -> Response:
    async with QuestionManager(database_session) as question_manager:
        question = await question_manager.delete_question(user, question)

    return Response()


@question_router.get(
    '/{question_id}/images/',
    status_code=200
)
async def get_image(
    question_id: int,
    user: User = Depends(get_current_user),
    database_session: AsyncSession = Depends(get_session)
) -> StreamingResponse:
    async with QuestionManager(database_session) as question_manager:
        image = await question_manager.get_image(question_id)
        byte_data = await get_file(MEDIA_ROOT + image.path)

    return StreamingResponse(io.BytesIO(byte_data), media_type=image.content_type)


@question_router.post(
    '/{question_id}/images/',
    status_code=201
)
async def create_image(
    question_id: int,
    user: User = Depends(get_current_user),
    files: List[UploadFile] = File(...),
    database_session: AsyncSession = Depends(get_session)
) -> Response:
    async with QuestionManager(database_session) as question_manager:
        for file in files:
            byte_data = await file.read()

            image_structure = ImageSchema(
                path=file.filename,
                content_type=file.content_type,
                question=question_id
            )
            await save_file(MEDIA_ROOT + file.filename, byte_data)
            await question_manager.create_image(image_structure)

    return Response(status_code=201)

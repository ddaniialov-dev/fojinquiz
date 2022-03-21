import io
from typing import List

from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Response
from starlette.responses import StreamingResponse

from crud import QuestionManager
from schemas import UpdateQuestion, CreateQuestion, GetQuestion, ImageSchema
from quiz_project import (
    JwtAccessRequired,
    get_session,
    token_header,
    save_file,
    MEDIA_ROOT, get_current_user, get_file
)


question_router = APIRouter(
    prefix='/questions',
    tags=['questions'],
    dependencies=[Depends(token_header)]
)


@question_router.get(
    '/',
    status_code=200,
    response_model=List[GetQuestion]
)
@JwtAccessRequired()
async def get_questions(
    auth: AuthJWT = Depends(),
    database_session: AsyncSession = Depends(get_session)
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
@JwtAccessRequired()
async def create_question(
    question: CreateQuestion,
    auth: AuthJWT = Depends(),
    database_session: AsyncSession = Depends(get_session)
) -> GetQuestion:
    async with QuestionManager(database_session) as question_manager:
        user = await get_current_user(database_session, auth)
        question_object = await question_manager.create_question(user, question)


    return question_object


@question_router.get(
    '/{question_id}/',
    status_code=200,
    response_model=GetQuestion
)
@JwtAccessRequired()
async def get_question(
    question_id: int,
    auth: AuthJWT = Depends(),
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
@JwtAccessRequired()
async def update_question(
    question: UpdateQuestion,
    auth: AuthJWT = Depends(),
    database_session: AsyncSession = Depends(get_session)
) -> GetQuestion:
    async with QuestionManager(database_session) as question_manager:
        question = await question_manager.update_question(question)

    return question


@question_router.delete(
    '/{question_id}/',
    status_code=204,
)
@JwtAccessRequired()
async def delete_question(
    question: UpdateQuestion,
    auth: AuthJWT = Depends(),
    database_session: AsyncSession = Depends(get_session)
) -> Response:
    async with QuestionManager(database_session) as question_manager:
        question = await question_manager.delete_question(question)

    return Response()


@question_router.get(
    '/{question_id}/images/',
    status_code=200
)
@JwtAccessRequired()
async def get_image(
    question_id: int,
    auth: AuthJWT = Depends(),
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
@JwtAccessRequired()
async def create_image(
    question_id: int,
    auth: AuthJWT = Depends(),
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

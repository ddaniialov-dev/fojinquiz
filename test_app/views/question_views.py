from typing import List

from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Response

from crud import QuestionManager
from schemas import UpdateQuestion, CreateQuestion, GetQuestion
from quiz_project import (
    JwtAccessRequired,
    get_session,
    token_header,
    save_file,
    MEDIA_ROOT, get_current_user
)


question_router = APIRouter(
    prefix='/questions',
    tags=['questions'],
    dependencies=[Depends(token_header)]
)


@question_router.post(
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
    response_model=CreateQuestion
)
@JwtAccessRequired()
async def create_question(
    question: CreateQuestion,
    auth: AuthJWT = Depends(),
    database_session: AsyncSession = Depends(get_session)
) -> CreateQuestion:
    async with QuestionManager(database_session) as question_manager:
        user = get_current_user(database_session, auth)
        question = await question_manager.create_question(user, question)

    return question


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

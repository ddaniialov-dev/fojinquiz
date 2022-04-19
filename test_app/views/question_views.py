import io
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, UploadFile, File, Response
from starlette.responses import StreamingResponse

from test_app.crud import QuestionManager
from test_app.schemas import UpdateQuestion, CreateQuestion, GetQuestion, ImageSchema
from test_app.checks import check_if_exist, check_if_exists, check_if_holder, check_if_test_has_question

from quiz_project.conf import Settings
from quiz_project.database import get_session
from quiz_project.utils.functions import save_file, get_file
from quiz_project.utils.dependencies import get_current_user
from user_app.models import User


question_router = APIRouter(
    prefix='/tests/{test_id}/questions',
    tags=['questions'],
)


@question_router.get(
    '/',
    status_code=200,
    response_model=List[GetQuestion]
)
async def get_questions(
    test_id: int,
    auth: User = Depends(get_current_user),
    database_session: AsyncSession = Depends(get_session),
) -> List[GetQuestion]:
    async with QuestionManager(database_session) as question_manager:
        questions = await question_manager.get_questions(test_id)
        await check_if_exist(questions)
        return questions


@question_router.post(
    '/',
    status_code=201,
    response_model=GetQuestion
)
async def create_question(
    question: CreateQuestion,
    test_id: int,
    auth: User = Depends(get_current_user),
    database_session: AsyncSession = Depends(get_session)
) -> GetQuestion:
    async with QuestionManager(database_session) as question_manager:
        test = await question_manager.get_test(test_id)
        await check_if_exists(test)
        await check_if_holder(auth.id, test.holder_id)
        question_object = await question_manager.create_question(question, test_id)
        return question_object

@question_router.get(
    '/{question_id}/',
    status_code=200,
    response_model=GetQuestion
)
async def get_question(
    question_id: int,
    test_id: int,
    auth: User = Depends(get_current_user),
    database_session: AsyncSession = Depends(get_session)
) -> GetQuestion:
    async with QuestionManager(database_session) as question_manager:
        test = await question_manager.get_test(test_id)
        await check_if_exists(test)
        question = await question_manager.get_question(question_id)
        await check_if_exists(question)
        await check_if_test_has_question(test_id, question)
        return question


@question_router.put(
    '/{question_id}/',
    status_code=200,
    response_model=GetQuestion
)
async def update_question(
    question: UpdateQuestion,
    question_id: int,
    test_id: int,
    auth: User = Depends(get_current_user),
    database_session: AsyncSession = Depends(get_session)
) -> GetQuestion:
    async with QuestionManager(database_session) as question_manager:
        test = await question_manager.get_test(test_id)
        await check_if_exists(test)
        await check_if_holder(auth.id, test.holder_id)
        question_object = await question_manager.get_question(question_id)
        await check_if_exists(question_object)
        await check_if_test_has_question(test_id, question_object)
        question = await question_manager.update_question(question.dict(exclude_unset=True), question_id)
        return question


@question_router.delete(
    '/{question_id}/',
    status_code=204,
)
async def delete_question(
    question_id: int,
    test_id: int,
    auth: User = Depends(get_current_user),
    database_session: AsyncSession = Depends(get_session)
) -> Response:
    async with QuestionManager(database_session) as question_manager:
        test = await question_manager.get_test(test_id)
        await check_if_exists(test)
        await check_if_holder(auth.id, test.holder_id)
        question_object = await question_manager.get_question(question_id)
        await check_if_exists(question_object)
        await check_if_test_has_question(test_id, question_object)
        await question_manager.delete_question(question_id)
        return Response(status_code=204)


@question_router.get(
    '/{question_id}/images/',
    status_code=200
)
async def get_image(
    question_id: int,
    auth: User = Depends(get_current_user),
    database_session: AsyncSession = Depends(get_session)
) -> StreamingResponse:
    async with QuestionManager(database_session) as question_manager:
        image = await question_manager.get_image(question_id)
        byte_data = await get_file(Settings.MEDIA_ROOT + image.path)

    return StreamingResponse(io.BytesIO(byte_data), media_type=image.content_type)


@question_router.post(
    '/{question_id}/images/',
    status_code=201
)
async def create_image(
    question_id: int,
    auth: User = Depends(get_current_user),
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
            await save_file(Settings.MEDIA_ROOT + file.filename, byte_data)
            await question_manager.create_image(image_structure)

    return Response(status_code=201)

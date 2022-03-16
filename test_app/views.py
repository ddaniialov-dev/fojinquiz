from typing import List

from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File

from .crud import TestManager
from quiz_project import (JwtAccessRequired, get_session,
                          token_header, get_current_user)
from test_app.schemas import TestGet, TestCreate, TestUpdate
from test_app.schemas import TestSchema
from quiz_project import JwtAccessRequired, get_session, token_header, MEDIA_ROOT, save_file

from quiz_project import JwtAccessRequired, get_session, token_header


test_router = APIRouter(
    prefix='/tests',
    tags=['tests'],
    dependencies=[Depends(token_header)]
)


@test_router.get(
    '/',
    status_code=200,
    response_model=List[TestGet]
)
@JwtAccessRequired()
async def get_user_tests(
    auth: AuthJWT = Depends(),
    database_session: AsyncSession = Depends(get_session)
) -> List[TestGet]:
    user = await get_current_user(database_session, auth)
    async with TestManager(database_session) as test_manager:
        tests = await test_manager.get_user_tests(user.id)

        if not tests:
            raise HTTPException(
                status_code=404, detail='data not found'
            )

    return tests


@router.get(
    '/all/',
    status_code=200,
    response_model=List[TestGet]
)
@JwtAccessRequired()
async def get_all_tests(
    auth: AuthJWT = Depends(),
    database_session: AsyncSession = Depends(get_session)
) -> List[TestGet]:
    async with TestManager(database_session) as test_manager:
        tests = await test_manager.get_tests()

        if not tests:
            raise HTTPException(
                status_code=404, detail='data not found'
            )

    return tests


@test_router.post(
    '/',
    status_code=201,
    response_model=TestGet
)
@JwtAccessRequired()
async def create_test(
    test: TestCreate,
    auth: AuthJWT = Depends(),
    database_session: AsyncSession = Depends(get_session)
) -> int:
    user = await get_current_user(database_session, auth)
    async with TestManager(database_session) as test_manager:
        test.holder = user.id
        result = await test_manager.create_test(test)
        if not result:
            raise HTTPException(
                status_code=400, detail='test wat not created'
            )
    return result



@test_router.delete(
    '/{test_id}/',
    status_code=204,
)
@JwtAccessRequired()
async def delete_test(
    test_id: int,
    auth: AuthJWT = Depends(),
    database_session: AsyncSession = Depends(get_session)
) -> None:
    user = await get_current_user(database_session, auth)
    async with TestManager(database_session) as test_manager:
        result = await test_manager.delete_test(user, test_id)

    if not result:
        raise HTTPException(status_code=404, detail="data not found")

    return Response()


@router.get(
    '/{test_id}/',
    status_code=200
)
@JwtAccessRequired()
async def get_test(
   test_id: int,
   auth: AuthJWT = Depends(),
   database_session: AsyncSession = Depends(get_session)
):
    async with TestManager(database_session) as test_manager:
        result =  await test_manager.get_test(test_id)
    
    if not result:
        raise HTTPException(
            status_code=404, detail="data not found"
        )
    return result


@router.put(
    '/{test_id}/',
    response_model=TestUpdate,
    status_code=200
)
async def update_test(
    test_id: int,
    test: TestUpdate,
    auth: AuthJWT = Depends(),
    database_session: AsyncSession = Depends(get_session)
):
    user = await get_current_user(database_session, auth)
    test.holder = user.id
    async with TestManager(database_session) as test_manager:
        result =  await test_manager.update_test(user, test_id, test.dict())
    
    if not result:
        raise HTTPException(
            status_code=404, detail="data not found"
        )
    return result


question_router = APIRouter(
    prefix='/questions',
    tags=['questions'],
    dependencies=[Depends(token_header)]
)


@question_router.post(
    '/questions/'
)
@JwtAccessRequired()
async def get_questions():
    pass


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

        async with QuestionManager(database_session) as test_manager:
            save_file(MEDIA_ROOT + file.filename, byte_data)
            image_structure = {
                'path': file.filename,
                'content_type': file.content_type,
                'question': question_id
            }
            test_manager.create_image(image_structure)

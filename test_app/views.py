import functools
from fastapi import APIRouter
from fastapi import Depends
from fastapi_jwt_auth import AuthJWT

from sqlalchemy.ext.asyncio import AsyncSession


from quiz_project import get_session
from test_app.schemas import TestSchema

from quiz_project import token_header
from quiz_project import AuthJWTWrapper

from .crud import TestManager

router = APIRouter(
    prefix="/tests",
    tags=['tests'],
    dependencies=[Depends(token_header)]
)


@router.post("/")
@AuthJWTWrapper()
def create_test(
    test: TestSchema,
    auth: AuthJWT = Depends(),
    database_session: AsyncSession = Depends(get_session)
):
    manager = TestManager(database_session)
    db_test = manager.create_test(test)
    return db_test

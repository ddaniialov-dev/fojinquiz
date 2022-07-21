from fastapi import HTTPException

from test_app.models import Question, Session


async def check_if_not_question(
        session_object: Session,
        question: Question,
):
    if not session_object.questions:
        raise HTTPException(
            status_code=404, detail='No questions for this session'
        )
    if question not in session_object.questions:
        raise HTTPException(
            status_code=404, detail='No question for this session'
        )

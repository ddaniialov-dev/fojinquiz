from fastapi import HTTPException

from test_app.models import Question


async def check_if_test_has_question(test_id: int, question: Question) -> None:
    if question.test_id != test_id:
        raise HTTPException(
            status_code=400, detail="Question not for this test.")

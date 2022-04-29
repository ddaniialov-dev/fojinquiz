from fastapi import HTTPException

from test_app.models import Answer


async def check_if_question_has_answer(question_id: int, answer: Answer) -> None:
    if answer.question_id != question_id:
        raise HTTPException(status_code=400, detail="Answer not for this question.")

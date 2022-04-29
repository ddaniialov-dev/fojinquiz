from fastapi import HTTPException

from test_app.models import Session


async def check_if_test_has_session(test_id: int, session: Session) -> None:
    if session.test_id != test_id:
        raise HTTPException(status_code=400, detail="Session not for this test.")

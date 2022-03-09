from fastapi import Header, HTTPException


def token_header(token: str = Header(...)):
    if not token:
        return HTTPException(
            status_code=400, detail='authentication credentials are not provided'
        )

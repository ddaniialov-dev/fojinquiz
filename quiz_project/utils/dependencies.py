from fastapi import Header, HTTPException


def token_header(authorization: str = Header(...)):
    if not authorization:
        return HTTPException(
            status_code=400, detail='authentication credentials are not provided'
        )

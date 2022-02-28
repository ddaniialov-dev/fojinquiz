from fastapi import Header, HTTPException


async def token_header(token: str = Header(...)):
    if not token:
        raise HTTPException(
            status_code=400, detail='authentication credentials are not provided'
        )

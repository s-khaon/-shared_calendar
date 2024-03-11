from fastapi import Header, HTTPException


async def get_token_header(authorization: str = Header()):
    if authorization is None or authorization == '':
        raise HTTPException(status_code=400, detail="Authorization header invalid")

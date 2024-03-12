from typing import Annotated

from fastapi import Header, HTTPException, Query

from entity import schemas


async def get_token_header(authorization: str = Header()):
    if authorization is None or authorization == '':
        raise HTTPException(status_code=400, detail="Authorization header invalid")


def get_page_query(
        page: Annotated[int, Query(gt=0)] = 1,
        size: Annotated[int, Query(le=100, gt=0)] = 20
) -> schemas.PageQuery:
    return schemas.PageQuery(page=page, size=size)

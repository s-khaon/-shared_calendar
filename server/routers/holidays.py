from typing import Annotated

from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session

from database import get_db
from entity import schemas
from service import holidays as holiday_service

router = APIRouter(
    prefix="/api/holidays",
    tags=["holidays"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.Holiday], name="节假日列表")
async def get_items(from_date: Annotated[str | None, Query(title="起始日期", regex=r"^\d{4}-\d{2}-\d{2}$")] = None,
                    to_date: Annotated[str | None, Query(title="截止日期", regex=r"^\d{4}-\d{2}-\d{2}$")] = None,
                    db: Session = Depends(get_db)):
    return holiday_service.get_holidays(from_date, to_date, db)

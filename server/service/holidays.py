import datetime
import requests

from sqlalchemy.orm import session

from config.config import Config
from entity import schemas, models


def get_holidays(from_date_str: str, to_date_str: str, db: session) -> list[schemas.Holiday]:
    # 检查数据库中是否有节假日信息
    if not db.query(models.Holiday).filter(models.Holiday.start_date >= datetime.date.today()).count():
        for url in Config.holidays_subscribe_urls:
            is_ok = fetch_and_save_holidays(url, db)
            if is_ok:
                break
    query = db.query(models.Holiday)
    if from_date_str:
        query = query.filter(models.Holiday.start_date >= from_date_str)
    if to_date_str:
        query = query.filter(models.Holiday.end_date <= to_date_str)
    return query.all()


def fetch_and_save_holidays(url, db: session) -> bool:
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        years_data = data.get('Years', {})
        holidays_data = []
        for year, holidays in years_data.items():
            for holiday in holidays:
                holiday_obj = models.Holiday(
                    name=holiday['Name'],
                    start_date=datetime.datetime.strptime(holiday['StartDate'], "%Y-%m-%d").date(),
                    end_date=datetime.datetime.strptime(holiday['EndDate'], "%Y-%m-%d").date(),
                    comp_days=holiday['CompDays'],
                    memo=holiday['Memo']
                )
                holidays_data.append(holiday_obj)
        if len(holidays_data) > 0:
            db.query(models.Holiday).delete()
        # 将数据存入数据库
        db.add_all(holidays_data)
        db.commit()
        db.flush()
        return True
    return False

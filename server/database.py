from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config.config import Config

SQLALCHEMY_DATABASE_URL = Config.db_url

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args=Config.connect_args, echo=Config.echo_sql
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

Base.metadata.create_all(engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

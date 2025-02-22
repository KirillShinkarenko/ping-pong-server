from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.repositories.db_time_storage_impl import DataBaseTimeRepositoryImpl
from app.repositories.time_storage import TimeRepository


# Зависимость для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Зависимость для SQLAlchemy репозитория
def get_sqlalchemy_repo(db: Session = Depends(get_db)) -> TimeRepository:
    return DataBaseTimeRepositoryImpl(db)

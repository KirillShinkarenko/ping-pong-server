from datetime import datetime
from sqlalchemy import Column, Integer, DateTime
from app.database import Base


class TimeRecord(Base):
    __tablename__ = "time_records"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

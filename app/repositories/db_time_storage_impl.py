from datetime import datetime
from typing import Dict, List
from sqlalchemy.orm import Session
from app.models.time_record import TimeRecord
from app.repositories.time_storage import TimeRepository


class DataBaseTimeRepositoryImpl(TimeRepository):
    def __init__(self, session: Session):
        self.session = session

    def write_time(self, timestamp: datetime) -> Dict:
        try:
            new_record = TimeRecord(timestamp=timestamp)
            self.session.add(new_record)
            self.session.commit()
            self.session.refresh(new_record)
            return {"id": new_record.id, "timestamp": new_record.timestamp}
        except Exception:
            self.session.rollback()
            raise

    def read_all(self) -> List[Dict]:
        records = (
            self.session.query(TimeRecord).order_by(TimeRecord.timestamp.desc()).all()
        )
        return [{"id": r.id, "timestamp": r.timestamp.isoformat()} for r in records]

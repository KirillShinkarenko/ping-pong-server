from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict


class TimeRepository(ABC):
    @abstractmethod
    def write_time(self, timestamp: datetime) -> Dict:
        pass

    @abstractmethod
    def read_all(self) -> List[Dict]:
        pass

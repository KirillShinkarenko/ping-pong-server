from datetime import datetime

from app.models.time_format import TimeFormat


class DateTimeFormatter:
    HUMAN_READABLE_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(self, format: TimeFormat = TimeFormat.ISO):
        self.format = format

    def get_current_time(self, format: TimeFormat | None = None) -> str:
        """Возвращает текущее время в указанном формате"""
        fmt = format or self.format
        now = datetime.now()

        if fmt == TimeFormat.HUMAN:
            return now.strftime(self.HUMAN_READABLE_FORMAT)
        return now.isoformat()

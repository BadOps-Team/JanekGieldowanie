import datetime

class DateFormatter:
    BRITISH_DATE_FORMAT = '%y-%m-%d'

    @staticmethod
    def format_date(date: datetime.date, formatter: str|None = None) -> str:
        if formatter is None:
            return date.isoformat()
        return date.strftime(formatter)
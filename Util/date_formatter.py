import datetime

class DateFormatter:
    BRITISH_DATE_FORMAT = '%y-%m-%d'

    @staticmethod
    def format_date(date: datetime.date, formatter: str|None = None) -> str:
        if isinstance(date, str):
            return datetime.datetime.strptime(date, "%Y-%m-%d").date()
        if formatter is None:
            return date.isoformat()
        return date.strftime(formatter)
from .period import Period
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Self


@dataclass
class EstimationConfig:
    start_date: date
    end_date: date
    forecast_days: int
    lookback_days: int

    def data_period(self) -> Period:
        start = self.start_date - timedelta(self.lookback_days)
        return Period(start, self.end_date)
    
    def estimation_range(self, data_length) -> range:
        return range(data_length - self.lookback_days)

    @classmethod
    def from_json(cls, json_content: str) -> Self:
        return cls(
            start_date=date.fromisoformat(json_content['start_date']),
            end_date=date.fromisoformat(json_content['end_date']),
            forecast_days=json_content['forecast_days'],
            lookback_days=json_content['lookback_days']
        )
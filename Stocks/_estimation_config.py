from .period import Period
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Self


@dataclass
class EstimationConfig:
    start_date: date
    forecast_days: int
    lookback_days: int
    simulation_length: int

    def data_period(self) -> Period:
        start = self.start_date - timedelta(self.lookback_days)
        end = self.start_date + timedelta(self.simulation_length)
        return Period(start, end)
    
    def estimation_range(self, data_length) -> range:
        return range(data_length - self.lookback_days)

    @classmethod
    def from_json(cls, json_content: str) -> Self:
        return cls(
            start_date=date.fromisoformat(json_content['start_date']),
            forecast_days=json_content['forecast_days'],
            lookback_days=json_content['lookback_days'],
            simulation_length=json_content['simulation_length']
        )
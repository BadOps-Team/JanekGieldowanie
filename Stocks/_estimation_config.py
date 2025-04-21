from .period import Period
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Self


@dataclass
class EstimationConfig:
    start_date: date
    forecast_days: int
    estimation_period: int
    simulation_length: int

    def data_period(self) -> Period:
        start = self.start_date - timedelta(self.estimation_period)
        end = self.start_date + timedelta(self.simulation_length)
        return Period(start, end)
    
    def estimation_range(self, data_length) -> range:
        return range(data_length - self.estimation_period)

    @classmethod
    def from_json(cls, json_content: dict) -> Self:
        return cls(
            start_date=date.fromisoformat(json_content['start_date']),
            forecast_days=json_content['forecast_days'],
            estimation_period=json_content['estimation_period'],
            simulation_length=json_content['simulation_length']
        )
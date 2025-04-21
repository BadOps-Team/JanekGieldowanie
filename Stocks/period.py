from dataclasses import dataclass
from datetime import date


@dataclass
class Period:
    start: date
    end: date
from pydantic import BaseModel
from typing import Dict, Optional

from app.calculations.dto import Calculation as CalculationDTO


class SeriesData(BaseModel):
    year: str
    period: str
    period_name: str
    value: float

    class Config:
        orm_mode = True

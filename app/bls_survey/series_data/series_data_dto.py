from pydantic import BaseModel
from typing import Dict, Optional


class SeriesDataDTOPartial(BaseModel):
    year: str
    period: str
    period_name: str
    value: float

    class Config:
        from_attributes = True

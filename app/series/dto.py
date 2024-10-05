from pydantic import BaseModel
from typing import Dict, Optional

from app.series_data.dto import SeriesData as SeriesDataDTO


class Series(BaseModel):
    catalog_id: str
    catalog_title: str
    seasonality: str
    survey_name: str
    measure_data_type: str
    area: str
    item: str
    data: SeriesDataDTO

    class Config:
        orm_mode = True

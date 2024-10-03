from pydantic import BaseModel
from typing import List, Dict, Optional


# Model for catalog details
class Series(BaseModel):
    series_title: str
    series_id: str
    seasonality: str
    survey_name: str
    measure_data_type: str
    area: str
    item: str


# Model for calculations
class Calculations(BaseModel):
    pct_changes: Optional[Dict[str, str]]  # A dictionary for percentage changes
    net_changes: Optional[Dict[str, str]]  # A dictionary for net changes


# Model for series data, which includes calculations
class SeriesData(BaseModel):
    year: str
    period: str
    period_name: str
    value: str
    footnotes: Optional[List[Dict]]
    calculations: Optional[Calculations]


# Main series request model, includes catalog and data
class SeriesRequest(BaseModel):
    seriesID: str
    catalog: Series
    data: List[SeriesData]

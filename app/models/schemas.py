from typing import Dict, List, Optional

from pydantic import BaseModel


# Model for catalog details
class Series(BaseModel):
    series_title: str
    catalog_id: str
    seasonality: str
    survey_name: str
    measure_data_type: str
    area: str
    item: str


# Model for calculations
class Calculations(BaseModel):
    # A dictionary for percentage changes
    pct_changes: Optional[Dict[str, str]]
    net_changes: Optional[Dict[str, str]]  # A dictionary for net changes


# Model for series data, which includes calculations
class SeriesData(BaseModel):
    year: str
    period: str
    period_name: str
    value: str
    footnotes: Optional[List[Dict]]
    calculations: Optional[Calculations]


# change the mapping so that catalog doesnt exist
# essentially we just have a series object that access directly
# how will this work with SeriesRequest. do you access SeriesRequest?

# Main series request model, includes catalog and data
class SeriesRequest(BaseModel):
    # catalog_id: int
    series: Series
    series_data: List[SeriesData]
    calculations: Calculations

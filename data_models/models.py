from typing import List, Optional

from pydantic import BaseModel


class Calculations(BaseModel):
    pct_changes: Optional[dict]
    net_changes: Optional[dict]


class Footnotes(BaseModel):
    footnote: Optional[dict] = {}


class SeriesData(BaseModel):
    year: str
    period: str
    periodName: str
    value: str
    footnotes: List[Footnotes]
    calculations: Calculations


class Catalog(BaseModel):
    series_title: str
    series_id: str
    seasonality: str
    survey_name: str
    survey_abbreviation: str
    measure_data_type: str
    area: str
    item: str


class Series(BaseModel):
    seriesID: str
    catalog: Catalog
    data: List[SeriesData]


class Results(BaseModel):
    series: List[Series]


class ResponseData(BaseModel):
    status: str
    responseTime: int
    message: List[str]
    Results: Results


class APIResponse(BaseModel):
    status: int
    data: ResponseData

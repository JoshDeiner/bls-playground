from pydantic import BaseModel
from typing import List
from app.bls_survey.calculations.calculation_dto import CalculationDTO

# DTO for the series data with calculations
class SeriesDataDTOFull(BaseModel):
    year: str
    period: str
    period_name: str
    value: float
    calculations: CalculationDTO

    class ConfigDict:
        from_attributes = True


# DTO for the series object
class SeriesDTO(BaseModel):
    catalog_id: str
    catalog_title: str
    seasonality: str
    survey_name: str
    measure_data_type: str
    area: str
    item: str
    data: List[SeriesDataDTOFull]  # Update to a list

    class ConfigDict:
        from_attributes = True

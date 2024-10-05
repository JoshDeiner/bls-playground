# app/series_data/repository.py

from sqlalchemy.orm import Session
from app.bls_survey.models.series import Series
from app.bls_survey.models.series import SeriesData
from app.bls_survey.models.series import Calculations


class SeriesRepository:
    def __init__(self, db: Session):
        self.db = db

    # Method to fetch a single series by catalog_id
    def get_series_by_catalog_id(self, catalog_id: str):
        return self.db.query(Series).filter(Series.catalog_id == catalog_id).one_or_none()

    # Method to fetch all series data associated with a given series ID
    def get_series_data_by_series_id(self, series_id: int):
        return self.db.query(SeriesData).filter(SeriesData.series_id == series_id).all()

    # Method to fetch calculations for a specific series data
    def get_calculations_by_series_data_id(self, series_data_id: int):
        return self.db.query(Calculations).filter(Calculations.series_data_id == series_data_id).first()


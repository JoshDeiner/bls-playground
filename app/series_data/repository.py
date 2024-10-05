# app/series_data/repository.py

from sqlalchemy.orm import Session
from app.models.series import SeriesData

class SeriesDataRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_series_data(self):
        return self.db.query(SeriesData).all()

    def get_series_data_by_id(self, series_id: int):
        return self.db.query(SeriesData).filter(SeriesData.series_id == series_id).first()

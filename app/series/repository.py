# app/series_data/repository.py

from sqlalchemy.orm import Session
from app.models.series import Series

class SeriesRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_series_data(self):
        return self.db.query(Series).all()


# app/calculations/repository.py
from sqlalchemy.orm import Session
from app.models.series import Calculations

class CalculationsRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_calculations(self):
        return self.db.query(Calculations).all()

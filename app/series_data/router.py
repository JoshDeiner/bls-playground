# # API to handle series data updates


import logging
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.series_data.repository import SeriesDataRepository
from app.series_data.dto import SeriesDataDTOPartial

router = APIRouter()

# GET endpoint to retrieve all series data
@router.get("/series_data", response_model=List[SeriesDataDTOPartial])
def get_all_series_data(db: Session = Depends(get_db)):
    try:
        repository = SeriesDataRepository(db)
        series_data = repository.get_all_series_data()

        if not series_data:
            raise HTTPException(status_code=404, detail="No data found")

        return series_data

    except Exception as e:
        logging.error(f"Error retrieving series data: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
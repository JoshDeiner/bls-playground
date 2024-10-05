# # API to handle series data updates

import logging


from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from typing import List

from app.database import get_db
from app.bls_survey.calculations.calculations_repository import CalculationsRepository
from app.bls_survey.calculations.calculation_dto import CalculationDTO


calculations_router = APIRouter()



# GET endpoint to retrieve all calculations
@calculations_router.get("/calculations", response_model=List[CalculationDTO])
def get_all_calculations(db: Session = Depends(get_db)):
    try:
        # Use the repository to get the data
        calculations_repo = CalculationsRepository(db)
        calculations = calculations_repo.get_all_calculations()

        if not calculations:
            raise HTTPException(status_code=404, detail="No calculations data found")

        return calculations

    except Exception as e:
        logging.error(f"Error retrieving calculations data: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


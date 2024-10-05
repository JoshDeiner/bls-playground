# # API to handle series data updates

import logging


from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from typing import List

from app.database import get_db
from app.calculations.repository import CalculationsRepository
from app.calculations.dto import Calculation as CalculationSchema  # Import the Pydantic schema


router = APIRouter()



# GET endpoint to retrieve all calculations
@router.get("/calculations", response_model=List[CalculationSchema])
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


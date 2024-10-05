# Updated Series Router

import logging

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session
from app.database import get_db

from app.series.repository import SeriesRepository
from app.series.dto import Series as SeriesDTO

from app.series.services.bls_service import fetch_bls_series_data
from app.series.services.processing import map_bls_data_with_ids
from app.series.services.series_service import upsert_series_payload

router = APIRouter()

# POST endpoint to update series data
@router.post("/series/{catalog_id}")
async def update_series(catalog_id: str, db: Session = Depends(get_db)):
    try:
        # Fetch BLS data using the async function
        bls_data = await fetch_bls_series_data(catalog_id)

        # Map the BLS data to your SeriesRequest Pydantic model here
        logging.info("Request incoming")
        request = map_bls_data_with_ids(bls_data)
        logging.info("Post map BLS data")

        # Call the upsert_series_payload orchestrator function with the mapped data
        upsert_series_payload(request, db, catalog_id)

        logging.info("Successfully called upsert_series_payload")

        return {"status": "success", "message": "Series data updated successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# GET endpoint to retrieve series data by catalog_id
@router.get("/series/{catalog_id}", response_model=SeriesDTO)
def get_series(catalog_id: str, db: Session = Depends(get_db)):
    try:
        # Initialize repository
        repo = SeriesRepository(db)

        # Fetch the series by catalog_id
        db_series = repo.get_series_by_catalog_id(catalog_id)
        if not db_series:
            raise HTTPException(status_code=404, detail="Series not found")

        # Fetch all associated series data
        db_series_data = repo.get_series_data_by_series_id(db_series.id)
        if not db_series_data:
            raise HTTPException(status_code=404, detail="No series data found")

        # Prepare the response object
        response = {
            "catalog_id": db_series.catalog_id,
            "catalog_title": db_series.catalog_title,
            "seasonality": db_series.seasonality,
            "survey_name": db_series.survey_name,
            "measure_data_type": db_series.measure_data_type,
            "area": db_series.area,
            "item": db_series.item,
            "data": [],
        }

        # For each series data, fetch its associated calculations and append to the response
        for series_data in db_series_data:
            db_calculations = repo.get_calculations_by_series_data_id(series_data.id)

            # Add data point and calculations to the response
            series_data_response = {
                "year": series_data.year,
                "period": series_data.period,
                "period_name": series_data.period_name,
                "value": series_data.value,
                "calculations": {
                    "pct_changes": db_calculations.pct_changes if db_calculations else None,
                    "net_changes": db_calculations.net_changes if db_calculations else None,
                },
            }
            response["data"].append(series_data_response)

        return response

    except Exception as e:
        logging.error(f"Error retrieving series data: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

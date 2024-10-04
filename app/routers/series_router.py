import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.schemas import SeriesRequest
from app.models.series import Calculations, Series, SeriesData
from app.services.bls_service import fetch_bls_series_data
from app.services.processing import map_bls_data_with_ids
from app.services.series_service import upsert_series

router = APIRouter()

# API to handle series data updates


# this is probably not right. on the post we hit the 3rd party
# probably at least need to pass in an ID
@router.post("/series")
async def update_series(db: Session = Depends(get_db)):

    try:
        # ideal dode
        # bls_data = await fetch_bls_series_data("SUUR0000SA0")
        # You'd map the BLS data to your SeriesRequest Pydantic model here
        # srequest = map_bls_data_with_ids(bls_data)
        # print("series_request", srequest)

        # Fetch BLS data using the async function
        logging.info("pre bls hit")
        bls_data = await fetch_bls_series_data("SUUR0000SA0")
        # logging.info(bls_data)

        # logging.info(bls_data)

        # Map the BLS data to your SeriesRequest Pydantic model here
        logging.info("request incoming")
        request = map_bls_data_with_ids(bls_data)
        logging.info("post map bls data")

        # Call the upsert function with the mapped data
        upsert_series(request, db)

        logging.info(upsert_series)

        # mock object
        # request = map_bls_data_with_ids()
        # series = request.get("series", 1)
        # upsert_series(request, db)
        return {"status": "success",
                "message": "Series data updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Define the GET endpoint for retrieving series data by catalog_id
# SUUR0000SA0
@router.get("/series/{catalog_id}")
def get_series(catalog_id: str, db: Session = Depends(get_db)):
    # Fetch the series by catalog_id
    # is the first really necessary? catalog_id is supposed to be unique. so
    # theoretically should only be one in the table
    db_series = db.query(Series).filter(
        Series.catalog_id == catalog_id).one_or_none()

    if not db_series:
        raise HTTPException(status_code=404, detail="Series not found")

    # Fetch all associated series data
    # compary series_data id against parent id
    # ie series has a has many relationship with SeriesData
    db_series_data = (
        db.query(SeriesData).filter(SeriesData.series_id == db_series.id).all()
    )

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
        # empty data list bc will fill later with series_data after making
        "data": [],
    }

    # For each series data, fetch its associated calculations and append to
    # the response
    for series_data in db_series_data:
        db_calculations = (
            db.query(Calculations)
            .filter(Calculations.series_data_id == series_data.id)
            .first()
        )

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

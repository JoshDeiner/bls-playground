# app/routes.py

from fastapi import APIRouter
from app.bls_survey.series.series_router import series_router
from app.bls_survey.calculations.calculations_router import calculations_router
from app.bls_survey.series_data.series_data_router import series_data_router

# Create a main router to include all feature routers
router = APIRouter()

# Include all the individual feature routers
router.include_router(series_router)
router.include_router(calculations_router)
router.include_router(series_data_router)

# app/routes.py

from fastapi import APIRouter
from app.series.router import router as series_router
from app.calculations.router import router as calculations_router
from app.series_data.router import router as series_data_router

# Create a main router to include all feature routers
router = APIRouter()

# Include all the individual feature routers
router.include_router(series_router)
router.include_router(calculations_router)
router.include_router(series_data_router)

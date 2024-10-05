import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI

# local imports
from app.database import init_db
from app.series.router import router as series_router
from app.calculations.router import router as calculations_router
from app.series_data.router import router as series_data_router


load_dotenv()

# Set up basic logging configuration
logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.include_router(series_router)
app.include_router(calculations_router)
app.include_router(series_data_router)


KEY = os.getenv("REG_KEY")

@app.on_event("startup")
def startup_event():
    init_db()  # Create the tables if they don't exist


@app.get("/")
def home():
    return {"message": "Welcome to API entrypoint"}

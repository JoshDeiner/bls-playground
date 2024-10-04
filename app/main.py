import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI

# local imports
from app.database import init_db
from app.routers.series_router import router as series_router

load_dotenv()

# Set up basic logging configuration
logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.include_router(series_router)

KEY = os.getenv("REG_KEY")

@app.on_event("startup")
def startup_event():
    init_db()  # Create the tables if they don't exist


@app.get("/")
def home():
    return {"message": "Welcome to API entrypoint"}

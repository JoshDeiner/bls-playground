import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI

# local imports
from app.database import init_db

# Import from routes
from app.routes import router as app_router  

load_dotenv()

# Set up basic logging configuration
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Include the combined router from app.routes
app.include_router(app_router)


KEY = os.getenv("REG_KEY")

@app.on_event("startup")
def startup_event():
    init_db()  # Create the tables if they don't exist


@app.get("/")
def home():
    return {"message": "Welcome to API entrypoint"}

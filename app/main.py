import logging
import structlog
import os
import yaml
import sys

from dotenv import load_dotenv
from fastapi import FastAPI

# local imports
from app.database import init_db

# Import from routes
from app.routes import router as app_router  

from logging_config import configure_logging
from logging_config import setup_structlog 


load_dotenv()


configure_logging()
setup_structlog()


app = FastAPI()

# Create a logger instance to use across the app
logger = structlog.get_logger()

# Include the combined router from app.routes
app.include_router(app_router)


KEY = os.getenv("REG_KEY")

APP_NAME = os.getenv("APP_NAME", "default-app-name")

@app.on_event("startup")
def startup_event():
    init_db()  # Create the tables if they don't exist
    logger.info("FastAPI startup", app_name=APP_NAME)


@app.get("/")
def home():
    # Step 4: Use structlog to log information about the root endpoint

    logger.info("Root endpoint accessed", endpoint="/", method="GET")
    return {"message": "Welcome to API entrypoint"}



if __name__ == "__main__":
    # Run Uvicorn directly, making sure logging works with Structlog
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, log_level="info")
import logging
import os
import yaml
import logging.config

from dotenv import load_dotenv
from fastapi import FastAPI

# local imports
from app.database import init_db

# Import from routes
from app.routes import router as app_router  

load_dotenv()


# Function to set up logging from a YAML file
def setup_logging_from_yaml(path: str):
    with open(path, 'r') as file:
        config = yaml.safe_load(file)
        # Dynamically replace the logger name with APP_NAME
        config['loggers'][APP_NAME] = config['loggers'].pop("myapp")
        logging.config.dictConfig(config)

# Set up basic logging configuration
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Include the combined router from app.routes
app.include_router(app_router)


KEY = os.getenv("REG_KEY")

APP_NAME = os.getenv("APP_NAME", "default-app-name")

# Set up logging from YAML configuration file
setup_logging_from_yaml('logging_config.yaml')


# Use the logger dynamically based on environment variable
logger = logging.getLogger(APP_NAME)
logger.info(f"FastAPI application '{APP_NAME}' has started")


@app.on_event("startup")
def startup_event():
    init_db()  # Create the tables if they don't exist


@app.get("/")
def home():
    logger.info("Root endpoint was accessed")
    return {"message": "Welcome to API entrypoint"}

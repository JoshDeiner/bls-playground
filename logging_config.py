# logging_config.py

import logging
import structlog
import sys

def configure_logging(log_file="app.log"):
    """Sets up logging to both file and console."""
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)

    logging.basicConfig(
        format="%(message)s",
        level=logging.INFO,
        handlers=[file_handler, stream_handler]
    )

def setup_structlog():
    """Sets up structlog with processors and JSON rendering."""
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.CallsiteParameterAdder(),
            structlog.processors.JSONRenderer(),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

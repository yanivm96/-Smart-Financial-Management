import logging
import os

# Logging configuration
DEBUG_MODE = False
LOGGING_LEVEL = logging.INFO if DEBUG_MODE else logging.ERROR
LOGGING_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

def configure_logging():
    logging.basicConfig(
        level=LOGGING_LEVEL,
        format=LOGGING_FORMAT,
        datefmt=DATE_FORMAT
    )
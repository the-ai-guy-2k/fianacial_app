import os
import logging
from datetime import datetime

LOG_DIR = os.path.join(os.path.dirname(__file__), '..', 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, 'app.log')

# Error classification
class ErrorCategory:
    CONFIG_ERROR = 'CONFIG_ERROR'
    API_KEY_ERROR = 'API_KEY_ERROR'
    FILE_UPLOAD_ERROR = 'FILE_UPLOAD_ERROR'
    CSV_PARSE_ERROR = 'CSV_PARSE_ERROR'
    OPENAI_API_ERROR = 'OPENAI_API_ERROR'
    STORAGE_ERROR = 'STORAGE_ERROR'
    VALIDATION_ERROR = 'VALIDATION_ERROR'


def setup_logger():
    logger = logging.getLogger('financial_app')
    if not logger.handlers:
        handler = logging.FileHandler(LOG_FILE)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


def log_error(category, message, error=None):
    logger = setup_logger()
    full_msg = f"[{category}] {message}"
    if error:
        full_msg += f" | Error: {str(error)}"
    logger.error(full_msg)
    return full_msg


def log_info(message):
    logger = setup_logger()
    logger.info(message)


def log_warning(message):
    logger = setup_logger()
    logger.warning(message)

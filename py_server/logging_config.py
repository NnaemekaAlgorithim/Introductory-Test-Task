import logging
from config import DEBUG, LOG_FILE

def configure_logging():
    if DEBUG == "true":
        # Set up console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

        # Set up file handler
        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

        # Configure root logger
        logging.basicConfig(level=logging.DEBUG, handlers=[console_handler, file_handler])
        logging.info("DEBUG mode enabled. Logging to console and file.")
    else:
        # Set up file handler
        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

        # Configure root logger
        logging.basicConfig(level=logging.INFO, handlers=[file_handler])
        logging.info("DEBUG mode disabled. Logging to file only.")

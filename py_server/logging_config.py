import logging
from typing import NoReturn
from py_server.config import DEBUG, LOG_FILE


"""
This module handles the configuration for logging.
"""


def configure_logging() -> NoReturn:
    """
    Configure logging for the application based
    on the DEBUG environment variable.

    The function sets up logging to both the
    console and a file if DEBUG mode is enabled.
    Otherwise, it logs only to a file at INFO level.
    The log file path is defined in the configuration.

    If DEBUG mode is enabled, logs are output to both
    the console and the file.
    If DEBUG mode is disabled, logs are output only to the file.

    Logging messages are formatted with timestamp,
    log level, and the log message.
    """
    # Common log format
    log_format = '%(asctime)s - %(levelname)s - %(message)s'

    # Ensure LOG_FILE is defined
    if not LOG_FILE:
        logging.basicConfig(
            level=logging.ERROR,
            format=log_format
        )
        logging.error(
            "LOG_FILE is not defined. Defaulting to console logging."
        )
        return

    try:
        # Set up the file handler
        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setFormatter(logging.Formatter(log_format))
    except (FileNotFoundError, PermissionError, OSError) as e:
        logging.basicConfig(
            level=logging.ERROR,
            format=log_format
        )
        logging.error(
            f"Failed to configure file handler for LOG_FILE: {e}"
        )
        return

    if DEBUG:
        try:
            # DEBUG mode is enabled, log to both console and file
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            console_handler.setFormatter(logging.Formatter(log_format))

            logging.basicConfig(
                level=logging.DEBUG,
                handlers=[console_handler, file_handler]
            )
            logging.info(
                "DEBUG mode enabled. Logging to console and file."
            )
        except Exception as e:
            logging.error(
                f"Failed to configure console handler: {e}"
            )
            logging.basicConfig(
                level=logging.ERROR,
                handlers=[file_handler]
            )
    else:
        try:
            # DEBUG mode is disabled, log only to file
            logging.basicConfig(
                level=logging.INFO,
                handlers=[file_handler]
            )
            logging.info(
                "DEBUG mode disabled. Logging to file only."
            )
        except Exception as e:
            logging.error(
                f"Failed to configure logging to file: {e}"
            )
            logging.basicConfig(
                level=logging.ERROR,
                format=log_format
            )

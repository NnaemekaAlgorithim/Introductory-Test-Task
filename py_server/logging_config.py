import logging
from typing import NoReturn
from py_server.config import DEBUG, LOG_FILE


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

    # Set up the file handler
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(logging.Formatter(log_format))

    if DEBUG:
        # DEBUG mode is enabled, log to both console and file
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(logging.Formatter(log_format))

        logging.basicConfig(
            level=logging.DEBUG,
            handlers=[console_handler, file_handler]
        )
        logging.info("DEBUG mode enabled. Logging to console and file.")
    else:
        # DEBUG mode is disabled, log only to file
        logging.basicConfig(
            level=logging.INFO,
            handlers=[file_handler]
        )
        logging.info("DEBUG mode disabled. Logging to file only.")

import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from the .env file
load_dotenv()

# Constants for server configuration
HOST: Optional[str] = os.getenv("HOST")
PORT: int = int(os.getenv("PORT", "0"))  # Default to 0 if not set
BUFFER_SIZE: int = int(os.getenv("BUFFER_SIZE", "1024"))  # Default to 1024 bytes
LOG_FILE: Optional[str] = os.getenv("LOG_FILE")
DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
FILE_PATH: Optional[str] = os.getenv("linuxpath")
REREAD_ON_QUERY: bool = os.getenv("REREAD_ON_QUERY", "false").lower() == "true"

# SSL Configuration
ENABLE_SSL: bool = os.getenv("ENABLE_SSL", "false").lower() == "true"
SSL_CERTIFICATE: Optional[str] = os.getenv("SSL_CERTIFICATE")
SSL_KEY: Optional[str] = os.getenv("SSL_KEY")
MAX_BUFFER_SIZE: int = int(os.getenv("MAX_BUFFER_SIZE", "4096"))  # Default to 4096 bytes


def validate_config() -> None:
    """
    Validate essential server configuration variables.

    Raises:
        ValueError: If required configuration variables are missing or invalid.
    """
    # Check the host and port
    if not HOST:
        raise ValueError("HOST is not set in the environment variables.")
    if not (1 <= PORT <= 65535):
        raise ValueError("PORT must be a positive integer between 1 and 65535.")

    # Validate buffer size
    if not (1 <= BUFFER_SIZE <= MAX_BUFFER_SIZE):
        raise ValueError(
            f"BUFFER_SIZE must be a positive integer not exceeding {MAX_BUFFER_SIZE} bytes."
        )

    # Log file validation
    if not LOG_FILE:
        raise ValueError("LOG_FILE is not set in the environment variables.")

    # File path validation
    if not FILE_PATH or not os.path.isfile(FILE_PATH):
        raise ValueError(f"FILE_PATH '{FILE_PATH}' does not exist or is not a valid file.")

    # SSL settings validation
    if ENABLE_SSL:
        if not SSL_CERTIFICATE or not os.path.isfile(SSL_CERTIFICATE):
            raise ValueError("SSL_CERTIFICATE is required and must point to a valid file.")
        if not SSL_KEY or not os.path.isfile(SSL_KEY):
            raise ValueError("SSL_KEY is required and must point to a valid file.")


# Validate the configuration at startup
try:
    validate_config()
except ValueError as error:
    raise RuntimeError(f"Invalid server configuration: {error}")

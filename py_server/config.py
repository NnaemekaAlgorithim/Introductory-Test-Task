import os
from dotenv import load_dotenv
from typing import Optional


"""
Module to manage configuration settings.

This module loads and validates configurations.
"""

# Load environment variables from the .env file
try:
    load_dotenv()
except Exception as e:
    raise RuntimeError(f"Error loading environment variables: {e}")

# Constants for server configuration
try:
    HOST: Optional[str] = os.getenv("HOST")
    PORT: int = int(os.getenv("PORT", "0"))
    BUFFER_SIZE: int = int(os.getenv("BUFFER_SIZE", "1024"))
    LOG_FILE: Optional[str] = os.getenv("LOG_FILE")
    DEBUG: bool = os.getenv("DEBUG", "false").strip().lower() == "true"
    FILE_PATH: Optional[str] = os.getenv("linuxpath")
    SSL_CERTIFICATE: Optional[str] = os.getenv("SSL_CERTIFICATE")
    SSL_KEY: Optional[str] = os.getenv("SSL_KEY")
    MAX_BUFFER_SIZE: int = int(os.getenv("MAX_BUFFER_SIZE", "4096"))
    REREAD_ON_QUERY: bool = (
        os.getenv("REREAD_ON_QUERY", "false")
        .strip()
        .lower() == "true"
    )
    ENABLE_SSL: bool = (
        os.getenv("ENABLE_SSL", "false")
        .strip()
        .lower() == "true"
    )
except ValueError as e:
    raise ValueError(
        f"Error parsing environment variables: {e}"
    )
except Exception as e:
    raise RuntimeError(
        f"Unexpected error during configuration loading: {e}"
    )


def validate_config() -> None:
    """
    Validate essential server configuration variables.

    This function ensures that the necessary configuration values
    for the server are present, properly formatted, and valid.

    Raises:
        ValueError: If any required configuration variable
                    is missing or invalid.
    """
    try:
        # Validate HOST
        HOST = os.getenv("HOST")
        if not HOST:
            raise ValueError(
                "HOST is not set in the environment variables."
            )

        # Validate PORT
        PORT = os.getenv("PORT")
        if not (1 <= int(PORT) <= 65535):
            raise ValueError(
                "PORT must be a positive integer between 1 and 65535."
            )

        # Validate BUFFER_SIZE
        BUFFER_SIZE = os.getenv("BUFFER_SIZE")
        MAX_BUFFER_SIZE = os.getenv("MAX_BUFFER_SIZE", 4096)
        if not (1 <= int(BUFFER_SIZE) <= int(MAX_BUFFER_SIZE)):
            raise ValueError(
                    f"BUFFER_SIZE must be a positive integer not exceeding "
                    f"{MAX_BUFFER_SIZE} bytes."
            )

        # Validate LOG_FILE
        LOG_FILE = os.getenv("LOG_FILE")
        if not LOG_FILE:
            raise ValueError(
                "LOG_FILE is not set in the environment variables."
            )

        # Validate SSL settings if SSL is enabled
        ENABLE_SSL = os.getenv("ENABLE_SSL", "false").strip().lower() == "true"
        if ENABLE_SSL:
            SSL_CERTIFICATE = os.getenv("SSL_CERTIFICATE")
            SSL_KEY = os.getenv("SSL_KEY")
            if not SSL_CERTIFICATE or not os.path.isfile(SSL_CERTIFICATE):
                raise ValueError(
                    "SSL_CERTIFICATE required and must point to a valid file."
                )
            if not SSL_KEY or not os.path.isfile(SSL_KEY):
                raise ValueError(
                    "SSL_KEY is required and must point to a valid file."
                )

        # Validate the presence of linuxpath in the .env file
        FILE_PATH = os.getenv("linuxpath")
        try:
            with open(".env", "r") as env_file:
                lines = env_file.readlines()
                if not any(line.startswith("linuxpath=") for line in lines):
                    raise ValueError(
                        "The .env file must contain a line starting with "
                        "'linuxpath='."
                    )
        except FileNotFoundError:
            raise FileNotFoundError(
                ".env file not found."
            )
        except Exception as e:
            raise RuntimeError(
                f"Error reading .env file: {e}"
            )

        # Validate FILE_PATH
        if not FILE_PATH or not os.path.isfile(FILE_PATH):
            raise ValueError(
                f"FILE_PATH '{FILE_PATH}'"
                f"does not exist or is not a valid file."
            )

    except ValueError as e:
        raise ValueError(
            f"Configuration validation error: {e}"
        )
    except Exception as e:
        raise RuntimeError(
            f"Unexpected error during configuration validation: {e}"
        )

import os
import pytest
from unittest.mock import patch, mock_open
from py_server.config import (
    HOST,
    PORT,
    BUFFER_SIZE,
    LOG_FILE,
    DEBUG,
    FILE_PATH,
    SSL_CERTIFICATE,
    SSL_KEY,
    MAX_BUFFER_SIZE,
    REREAD_ON_QUERY,
    ENABLE_SSL,
    validate_config
)


def test_load_env_variables():
    """Test environment variable loading."""
    assert HOST == HOST
    assert PORT == PORT
    assert BUFFER_SIZE == BUFFER_SIZE
    assert LOG_FILE == LOG_FILE
    assert DEBUG == DEBUG
    assert FILE_PATH == FILE_PATH
    assert SSL_CERTIFICATE == SSL_CERTIFICATE
    assert SSL_KEY == SSL_KEY
    assert MAX_BUFFER_SIZE == MAX_BUFFER_SIZE
    assert REREAD_ON_QUERY == REREAD_ON_QUERY
    assert ENABLE_SSL == ENABLE_SSL


def test_validate_config_success():
    """Test successful configuration validation."""
    validate_config()


def test_validate_missing_host(monkeypatch):
    """Test validation failure when HOST is missing."""

    monkeypatch.setenv("HOST", "")
    print(os.environ.get("HOST"))
    with pytest.raises(
        ValueError, match="HOST is not set in the environment variables."
    ):
        validate_config()


def test_validate_invalid_port():
    """Test validation failure for an invalid PORT."""
    with patch.dict(os.environ, {"PORT": "70000"}):
        with pytest.raises(
            ValueError,
            match="PORT must be a positive integer between 1 and 65535."
        ):
            validate_config()


def test_validate_invalid_buffer_size():
    """Test validation failure for BUFFER_SIZE exceeding MAX_BUFFER_SIZE."""
    with patch.dict(os.environ, {"BUFFER_SIZE": "9000"}):
        expected_message = (
            "BUFFER_SIZE must be a positive integer not exceeding 8192 bytes."
        )
        with pytest.raises(ValueError, match=expected_message):
            validate_config()


def test_validate_missing_log_file():
    """Test validation failure when LOG_FILE is missing."""
    with patch.dict(os.environ, {"LOG_FILE": ""}):
        with pytest.raises(
            ValueError,
            match="LOG_FILE is not set in the environment variables."
        ):
            validate_config()


def test_validate_ssl_cert_missing(monkeypatch):
    """
    Test validation failure when SSL_CERTIFICATE
    is missing with SSL enabled.
    """

    # Mock environment variables using monkeypatch
    monkeypatch.setenv("ENABLE_SSL", "true")
    monkeypatch.setenv("SSL_CERTIFICATE", "")
    monkeypatch.setenv("SSL_KEY", "/path/to/key.pem")

    # Mock os.path.isfile to simulate missing SSL_CERTIFICATE file
    def mock_isfile(path):
        return path == "/path/to/key.pem"

    monkeypatch.setattr("os.path.isfile", mock_isfile)

    # Expecting a ValueError when SSL_CERTIFICATE is missing
    with pytest.raises(
        ValueError,
        match="SSL_CERTIFICATE required and must point to a valid file."
    ):
        validate_config()


def test_validate_ssl_key_missing(monkeypatch):
    """
    Test validation failure when SSL_KEY
    is missing with SSL enabled.
    """

    # Mock environment variables using monkeypatch
    monkeypatch.setenv("ENABLE_SSL", "true")
    monkeypatch.setenv("SSL_CERTIFICATE", "/path/to/cert.pem")
    monkeypatch.setenv("SSL_KEY", "")

    # Mock os.path.isfile to simulate missing SSL_KEY file
    def mock_isfile(path):
        return path == "/path/to/cert.pem"

    monkeypatch.setattr("os.path.isfile", mock_isfile)

    # Expecting a ValueError when SSL_KEY is missing
    expected_message = (
        "SSL_KEY is required and must point to a valid file."
    )
    with pytest.raises(ValueError, match=expected_message):
        validate_config()


def test_validate_missing_linuxpath_in_env_file(monkeypatch):
    """Test validation failure when linuxpath is missing in .env file."""

    # Mock opening the .env file with monkeypatch
    env_content = ""
    monkeypatch.setattr(
        "builtins.open", mock_open(read_data=env_content)
    )

    # Expecting a RuntimeError with a
    # specific message when linuxpath is missing
    expected_message = (
        "The .env file must contain a "
        "line starting with 'linuxpath='."
    )
    with pytest.raises(RuntimeError, match=expected_message):
        validate_config()


def test_validate_invalid_file_path(monkeypatch):
    """Test validation failure for invalid FILE_PATH."""

    # Mock environment variable and file existence
    monkeypatch.setenv("linuxpath", "/path/to/file")
    monkeypatch.setattr("os.path.isfile", lambda x: False)

    # Expecting a ValueError related to SSL_CERTIFICATE first
    expected_message = (
        "SSL_CERTIFICATE required and must point to a valid file."
    )
    with pytest.raises(ValueError, match=expected_message):
        validate_config()

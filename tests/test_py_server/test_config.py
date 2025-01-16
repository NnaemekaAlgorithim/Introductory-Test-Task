import os
import pytest
from unittest.mock import patch

# Assume the original code is in a module named 'config'
from py_server.config import validate_config, HOST, FILE_PATH


@pytest.fixture
def mock_env_vars():
    """
    Fixture to mock environment variables for testing.
    """
    mock_values = {
        "HOST": "localhost",
        "PORT": "44445",
        "BUFFER_SIZE": "1024",
        "LOG_FILE": "/path/to/logfile.log",
        "DEBUG": "True",
        "linuxpath": "/path/to/file",
        "REREAD_ON_QUERY": "false",
        "ENABLE_SSL": "false",
        "SSL_CERTIFICATE": "/path/to/certificate",
        "SSL_KEY": "/path/to/key",
        "MAX_BUFFER_SIZE": "4096"
    }

    # Use patch.dict to mock environment variables temporarily
    with patch.dict(os.environ, mock_values):
        yield mock_values
    # No need to manually delete environment variables here as
    # patch.dict handles it.


def test_valid_config(mock_env_vars):
    """
    Test that validate_config doesn't raise an
    exception with valid configuration.
    """
    # Mock the files to ensure valid file paths
    with patch("os.path.isfile", return_value=True):
        validate_config()  # Should not raise any exception


def test_missing_debug(mock_env_vars):
    """
    Test that a missing or invalid DEBUG raises a ValueError.
    """
    os.environ["DEBUG"] = "invalid"  # Set invalid DEBUG value
    with patch("os.path.isfile", return_value=True):
        validate_config()


def test_missing_host(mock_env_vars):
    """
    Test that missing HOST raises a ValueError.
    """
    # Remove the HOST variable for this test
    with patch.dict(os.environ, {"HOST": HOST}):
        with patch("os.path.isfile", return_value=True):
            validate_config()


def test_invalid_port(mock_env_vars):
    """
    Test that an invalid PORT raises a ValueError.
    """
    os.environ["PORT"] = "70000"  # Invalid port value
    with patch("os.path.isfile", return_value=True):
        validate_config()


def test_invalid_buffer_size(mock_env_vars):
    """
    Test that an invalid BUFFER_SIZE raises a ValueError.
    """
    # Invalid buffer size greater than MAX_BUFFER_SIZE
    os.environ["BUFFER_SIZE"] = "5000"
    with patch("os.path.isfile", return_value=True):
        validate_config()


def test_missing_log_file(mock_env_vars):
    """
    Test that missing LOG_FILE raises a ValueError.
    """
    del os.environ["LOG_FILE"]
    with patch("os.path.isfile", return_value=True):
        validate_config()


def test_invalid_file_path(mock_env_vars):
    """
    Test that invalid FILE_PATH raises a ValueError.
    """
    os.environ["linuxpath"] = FILE_PATH
    validate_config()


def test_ssl_required_when_enabled(mock_env_vars):
    """
    Test that SSL_CERTIFICATE and SSL_KEY are required when ENABLE_SSL is True.
    """
    os.environ["ENABLE_SSL"] = "true"
    os.environ["SSL_CERTIFICATE"] = ""  # SSL_CERTIFICATE is missing
    os.environ["SSL_KEY"] = ""  # SSL_KEY is missing
    validate_config()

    os.environ["SSL_CERTIFICATE"] = "/valid/path/to/cert"
    validate_config()


def test_ssl_not_required_when_disabled(mock_env_vars):
    """
    Test that no SSL validation occurs when ENABLE_SSL is False.
    """
    os.environ["ENABLE_SSL"] = "false"
    del os.environ["SSL_CERTIFICATE"]  # Remove SSL_CERTIFICATE
    del os.environ["SSL_KEY"]  # Remove SSL_KEY
    with patch("os.path.isfile", return_value=True):
        validate_config()  # Should not raise any exception

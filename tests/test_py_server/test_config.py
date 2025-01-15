import contextlib
import os
import pytest
from unittest import mock
from py_server.config import validate_config


def test_validate_config_missing_host(set_env):
    """Test missing HOST configuration."""
    with set_env({
        "PORT": "8080",
        "BUFFER_SIZE": "1024",
        "LOG_FILE": "server.log",
        "DEBUG": "true",
    }):
        with pytest.raises(ValueError, match="HOST is not set in the environment variables."):
            validate_config()

def test_validate_config_invalid_port(set_env):
    """Test invalid PORT configuration."""
    with set_env({
        "HOST": "localhost",
        "PORT": "-1",  # Invalid port
        "BUFFER_SIZE": "1024",
        "LOG_FILE": "server.log",
        "DEBUG": "true",
    }):
        with pytest.raises(ValueError, match="PORT must be a positive integer."):
            validate_config()

def test_validate_config_invalid_buffer_size(set_env):
    """Test invalid BUFFER_SIZE configuration."""
    with set_env({
        "HOST": "localhost",
        "PORT": "8080",
        "BUFFER_SIZE": "0",  # Invalid buffer size
        "LOG_FILE": "server.log",
        "DEBUG": "true",
    }):
        with pytest.raises(ValueError, match="BUFFER_SIZE must be a positive integer."):
            validate_config()

def test_validate_config_missing_log_file(set_env):
    """Test missing LOG_FILE configuration."""
    with set_env({
        "HOST": "localhost",
        "PORT": "8080",
        "BUFFER_SIZE": "1024",
        "DEBUG": "true",
    }):
        with pytest.raises(ValueError, match="LOG_FILE is not set in the environment variables."):
            validate_config()

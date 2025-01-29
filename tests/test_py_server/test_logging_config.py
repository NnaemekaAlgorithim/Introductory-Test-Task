import logging
import pytest
from unittest.mock import patch, MagicMock
from py_server.logging_config import configure_logging


@pytest.fixture
def mock_config():
    """Fixture to mock DEBUG and LOG_FILE."""
    with patch("py_server.logging_config.DEBUG", False), \
         patch("py_server.logging_config.LOG_FILE", "test_log_file.log"):
        yield


def test_no_log_file_defined():
    """Test behavior when LOG_FILE is not defined."""
    with patch("py_server.logging_config.LOG_FILE", None), \
         patch("logging.error") as mock_error, \
         patch("logging.basicConfig") as mock_basic:
        configure_logging()
        mock_basic.assert_called_once_with(
            level=logging.ERROR,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )
        mock_error.assert_called_once_with(
            "LOG_FILE is not defined. Defaulting to console logging."
        )


def test_file_handler_file_not_found():
    """Test behavior when the file handler raises FileNotFoundError."""
    with patch("py_server.logging_config.LOG_FILE", "invalid/path.log"), \
         patch("logging.FileHandler", side_effect=FileNotFoundError), \
         patch("logging.error") as mock_error, \
         patch("logging.basicConfig") as mock_basic:
        configure_logging()
        mock_basic.assert_called_once_with(
            level=logging.ERROR,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )
        assert mock_error.called
        error_message = mock_error.call_args[0][0]
        assert "Failed to configure file handler for LOG_FILE" in error_message


def test_file_handler_permission_error():
    """Test behavior when the file handler raises PermissionError."""
    with patch("py_server.logging_config.LOG_FILE", "test_log_file.log"), \
         patch("logging.FileHandler", side_effect=PermissionError), \
         patch("logging.error") as mock_error, \
         patch("logging.basicConfig") as mock_basic:
        configure_logging()
        mock_basic.assert_called_once_with(
            level=logging.ERROR,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )
        assert mock_error.called
        error_message = mock_error.call_args[0][0]
        assert "Failed to configure file handler for LOG_FILE" in error_message


def test_debug_mode_enabled(mock_config):
    """Test logging behavior when DEBUG is enabled."""
    with patch("py_server.logging_config.DEBUG", True), \
         patch("logging.StreamHandler") as mock_stream, \
         patch("logging.FileHandler") as mock_file, \
         patch("logging.basicConfig") as mock_basic, \
         patch("logging.info") as mock_info:
        mock_stream.return_value = MagicMock()
        mock_file.return_value = MagicMock()

        configure_logging()
        mock_basic.assert_called_once()
        mock_info.assert_called_with(
            "DEBUG mode enabled. Logging to console and file."
        )


def test_debug_mode_disabled(mock_config):
    """Test logging behavior when DEBUG is disabled."""
    with patch("logging.FileHandler") as mock_file, \
         patch("logging.basicConfig") as mock_basic, \
         patch("logging.info") as mock_info:
        mock_file.return_value = MagicMock()

        configure_logging()
        mock_basic.assert_called_once()
        mock_info.assert_called_with(
            "DEBUG mode disabled. Logging to file only."
        )


def test_console_handler_exception(mock_config):
    """Test behavior when console handler raises an exception in DEBUG mode."""
    with patch("py_server.logging_config.DEBUG", True), \
         patch("logging.StreamHandler",
               side_effect=Exception("Console handler error")), \
         patch("logging.FileHandler") as mock_file, \
         patch("logging.error") as mock_error, \
         patch("logging.basicConfig") as mock_basic:
        mock_file.return_value = MagicMock()

        configure_logging()
        mock_basic.assert_called_once()
        assert mock_error.called
        error_message = mock_error.call_args[0][0]
        assert "Failed to configure console handler" in error_message

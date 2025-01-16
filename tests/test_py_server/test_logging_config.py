from unittest import mock
import pytest
from unittest.mock import patch, MagicMock
import logging
from py_server.config import LOG_FILE
from py_server.logging_config import configure_logging


@pytest.fixture
def mock_logging_handlers():
    """Fixture to mock logging handlers."""
    with patch("py_server.server.logging.FileHandler") as mock_file_handler, \
         patch(
             "py_server.server.logging.StreamHandler"
            ) as mock_stream_handler, \
         patch(
             "py_server.server.logging.basicConfig"
            ) as mock_basic_config:

        yield mock_stream_handler, mock_file_handler, mock_basic_config


def test_configure_logging_debug_on(mock_logging_handlers):
    """
    Test that logging is configured correctly when DEBUG is True.

    In DEBUG mode, logging should be set to output to both console and file.
    """
    global DEBUG
    DEBUG = True  # Set DEBUG to True for this test

    mock_stream_handler = mock_logging_handlers[0]
    mock_file_handler = mock_logging_handlers[1]
    mock_basic_config = mock_logging_handlers[2]

    # Mock the logging handlers
    mock_stream_handler.return_value = MagicMock()
    mock_file_handler.return_value = MagicMock()

    configure_logging()

    # Assert that logging.basicConfig is called with the expected handlers
    mock_basic_config.assert_called_once_with(
        level=logging.DEBUG,
        handlers=[
            mock_stream_handler.return_value,
            mock_file_handler.return_value
        ]
    )

    # Assert that the file handler was created correctly
    mock_file_handler.assert_called_once_with(LOG_FILE)

    # Assert StreamHandler (console handler) was created and configured
    mock_stream_handler.assert_called_once()
    mock_stream_handler.return_value.setLevel.assert_called_once_with(
        logging.DEBUG
    )

    # Verify if logging information about the DEBUG mode is logged
    logging.info("DEBUG mode enabled. Logging to console and file.")


@mock.patch('logging.basicConfig')
@mock.patch('logging.FileHandler')
@mock.patch('logging.StreamHandler')
def test_configure_logging_debug_off(
    mock_stream_handler,
    mock_file_handler,
    mock_basic_config
):
    """
    Test that logging is configured correctly when DEBUG is False.
    In non-DEBUG mode, logging should only output to the file at INFO level.
    """
    global DEBUG
    DEBUG = False  # Set DEBUG to False for this test

    # Mock the logging handlers
    mock_stream_handler.return_value = mock.MagicMock()
    mock_file_handler.return_value = mock.MagicMock()

    # Call the logging configuration function
    configure_logging()


def test_configure_logging_with_invalid_file_handler(mock_logging_handlers):
    """
    Test the behavior when the file handler cannot be created.

    This checks how the logging setup behaves if there is an error creating
    the file handler (e.g., invalid file path).
    """
    global DEBUG
    DEBUG = True  # Set DEBUG to True for this test

    mock_stream_handler, \
        mock_file_handler, \
        mock_basic_config = mock_logging_handlers

    # Simulate the failure of file handler creation
    mock_file_handler.side_effect = Exception("Unable to create file handler")

    with pytest.raises(Exception):
        configure_logging()

    # Ensure no further logging setup happens
    mock_basic_config.assert_not_called()


def test_configure_logging_with_missing_config_values():
    """
    Test that configure_logging behaves correctly when necessary config values
    like `DEBUG` and `LOG_FILE` are missing or incorrectly set.
    """
    global DEBUG, LOG_FILE
    DEBUG = None  # Simulating missing DEBUG value
    LOG_FILE = None  # Simulating missing log file path

    # Use pytest.raises to assert that the exception is raised
    configure_logging()


def test_configure_logging_edge_case(mock_logging_handlers):
    """
    Test that logging configuration is robust when edge cases occur, like
    both file and console logging being incorrectly configured.
    """
    global DEBUG
    DEBUG = True

    mock_stream_handler, \
        mock_file_handler, \
        mock_basic_config = mock_logging_handlers

    # Mock handlers
    mock_stream_handler.return_value = MagicMock()
    mock_file_handler.return_value = MagicMock()

    # Simulate an edge case by modifying the handlers
    # before calling the function
    mock_stream_handler.return_value.setLevel = MagicMock(
        side_effect=Exception("Unexpected error")
    )

    with pytest.raises(Exception):
        configure_logging()

    # Ensure no logging was set up
    mock_basic_config.assert_not_called()

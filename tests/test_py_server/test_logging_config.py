# import pytest
# import logging
# from unittest import mock
# from py_server.logging_config import configure_logging
# from py_server.config import DEBUG, LOG_FILE

# @pytest.fixture
# def mock_debug_mode_enabled(monkeypatch):
#     """Mock the DEBUG environment variable to be True."""
#     monkeypatch.setenv("DEBUG", "true")
#     # Ensure the LOG_FILE is set properly for testing
#     monkeypatch.setenv("LOG_FILE", "test_log_file.log")

# def test_configure_logging_debug_mode(mock_debug_mode_enabled):
#     """Test logging configuration when DEBUG mode is enabled."""
#     # Set up mock handlers to capture log output
#     with mock.patch("logging.StreamHandler") as mock_stream_handler:
#         with mock.patch("logging.FileHandler") as mock_file_handler:
#             configure_logging()  # Call the function

#             # Assert that both file handler and console handler are configured
#             mock_stream_handler.assert_called_once()
#             mock_file_handler.assert_called_once()

#             # Check if the logging level is set to DEBUG for console and INFO for file
#             mock_stream_handler.return_value.setLevel.assert_called_with(logging.DEBUG)
#             mock_file_handler.return_value.setLevel.assert_called_with(logging.INFO)
            
#             # Verify that the info log was written for DEBUG mode enabled
#             logging.info.assert_any_call("DEBUG mode enabled. Logging to console and file.")

# @pytest.fixture
# def mock_debug_mode_disabled(monkeypatch):
#     """Mock the DEBUG environment variable to be False."""
#     monkeypatch.setenv("DEBUG", "false")
#     # Ensure the LOG_FILE is set properly for testing
#     monkeypatch.setenv("LOG_FILE", "test_log_file.log")

# def test_configure_logging_non_debug_mode(mock_debug_mode_disabled):
#     """Test logging configuration when DEBUG mode is disabled."""
#     # Set up mock handlers to capture log output
#     with mock.patch("logging.FileHandler") as mock_file_handler:
#         configure_logging()  # Call the function

#         # Assert that only file handler is configured (console handler should not be)
#         mock_file_handler.assert_called_once()
        
#         # Verify that the info log was written for DEBUG mode disabled
#         logging.info.assert_any_call("DEBUG mode disabled. Logging to file only.")

# def test_missing_log_file():
#     """Test logging configuration when LOG_FILE is not set."""
#     with mock.patch("os.getenv", return_value=None):
#         with pytest.raises(ValueError, match="LOG_FILE must be set in the environment variables"):
#             configure_logging()

# def test_invalid_debug_value(monkeypatch):
#     """Test for invalid DEBUG environment variable value."""
#     monkeypatch.setenv("DEBUG", "invalid_value")
#     monkeypatch.setenv("LOG_FILE", "test_log_file.log")
    
#     with mock.patch("logging.FileHandler") as mock_file_handler:
#         with mock.patch("logging.StreamHandler") as mock_stream_handler:
#             configure_logging()  # Call the function

#             # Ensure logging is only to file when DEBUG is invalid
#             mock_stream_handler.assert_not_called()
#             mock_file_handler.assert_called_once()
#             logging.info.assert_any_call("DEBUG mode disabled. Logging to file only.")

# def test_file_handler_configuration(mock_debug_mode_enabled):
#     """Test that the file handler is configured with the correct log level."""
#     with mock.patch("logging.FileHandler") as mock_file_handler:
#         configure_logging()  # Call the function

#         # Ensure the file handler was configured
#         mock_file_handler.assert_called_once()
#         # Check that the file handler's log level is INFO
#         mock_file_handler.return_value.setLevel.assert_called_with(logging.INFO)

# def test_logging_format(mock_debug_mode_enabled):
#     """Test that the correct log format is set."""
#     with mock.patch("logging.FileHandler") as mock_file_handler:
#         with mock.patch("logging.StreamHandler") as mock_stream_handler:
#             configure_logging()  # Call the function

#             # Verify that both handlers are using the correct log format
#             mock_stream_handler.return_value.setFormatter.assert_called_with(mock.ANY)
#             mock_file_handler.return_value.setFormatter.assert_called_with(mock.ANY)
            
#             # Check that the log format is what we expect
#             expected_format = '%(asctime)s - %(levelname)s - %(message)s'
#             mock_stream_handler.return_value.setFormatter.assert_called_with(logging.Formatter(expected_format))

# def test_invalid_log_file_path(monkeypatch):
#     """Test logging when the log file path is invalid."""
#     monkeypatch.setenv("DEBUG", "true")
#     monkeypatch.setenv("LOG_FILE", "/invalid/path/to/logfile.log")

#     with pytest.raises(OSError, match="Failed to open log file"):
#         configure_logging()

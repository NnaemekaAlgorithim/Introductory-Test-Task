# import pytest
# from unittest import mock
# from py_server.server import start_server, get_file_path_and_reread_option
# from py_server.config import HOST, PORT, FILE_PATH, REREAD_ON_QUERY

# @pytest.fixture
# def mock_valid_configuration(monkeypatch):
#     """Mock valid configuration settings."""
#     monkeypatch.setenv("FILE_PATH", "/valid/path/to/file")
#     monkeypatch.setenv("REREAD_ON_QUERY", "true")
#     monkeypatch.setenv("HOST", "localhost")
#     monkeypatch.setenv("PORT", "8080")

# def test_server_startup(mock_valid_configuration):
#     """Test that the server starts up successfully with valid configuration."""
#     with mock.patch("socket.socket") as mock_socket:
#         with mock.patch("logging.info") as mock_logging:
#             start_server()  # Call the function to start the server

#             # Check that the server socket was created and bound
#             mock_socket.assert_called_once_with(mock.ANY, mock.ANY)
#             mock_socket.return_value.bind.assert_called_once_with((HOST, PORT))

#             # Verify that the server logs the startup message
#             mock_logging.assert_any_call(f"Server started on {HOST}:{PORT}")

# @pytest.fixture
# def mock_invalid_configuration(monkeypatch):
#     """Mock invalid configuration settings."""
#     monkeypatch.setenv("FILE_PATH", "")
#     monkeypatch.setenv("REREAD_ON_QUERY", "true")

# def test_server_startup_invalid_file_path(mock_invalid_configuration):
#     """Test that the server does not start if the file path is invalid."""
#     with mock.patch("logging.error") as mock_logging:
#         start_server()  # Call the function to start the server

#         # Verify that the error message is logged when no valid file path is provided
#         mock_logging.assert_any_call("Server cannot start without a valid file path.")

# def test_client_connection_handling(mock_valid_configuration):
#     """Test that the server creates a new thread for each incoming client connection."""
#     with mock.patch("socket.socket") as mock_socket:
#         with mock.patch("threading.Thread") as mock_thread:
#             mock_socket.return_value.accept.return_value = ("client_socket", ("127.0.0.1", 12345))
#             start_server()  # Call the function to start the server

#             # Check that the server attempts to accept connections
#             mock_socket.return_value.accept.assert_called_once()

#             # Ensure that a new thread is created for the client connection
#             mock_thread.assert_called_once_with(
#                 target=mock.ANY,
#                 args=("client_socket", ("127.0.0.1", 12345), FILE_PATH, REREAD_ON_QUERY, [])
#             )

# def test_server_shutdown(mock_valid_configuration):
#     """Test that the server shuts down gracefully on a KeyboardInterrupt."""
#     with mock.patch("socket.socket") as mock_socket:
#         with mock.patch("logging.info") as mock_logging:
#             # Simulate a KeyboardInterrupt exception
#             with mock.patch("builtins.input", side_effect=KeyboardInterrupt):
#                 start_server()

#                 # Verify that the server shutdown message is logged
#                 mock_logging.assert_any_call("Server shutting down...")

#                 # Ensure that the server socket is closed after shutdown
#                 mock_socket.return_value.close.assert_called_once()
#                 mock_logging.assert_any_call("Server socket closed.")

# def test_server_runtime_error(mock_valid_configuration):
#     """Test that errors during server runtime are logged."""
#     with mock.patch("socket.socket") as mock_socket:
#         with mock.patch("logging.error") as mock_logging:
#             # Simulate an exception being raised when the server tries to accept a connection
#             mock_socket.return_value.accept.side_effect = Exception("Simulated error")
#             start_server()

#             # Verify that the error message is logged
#             mock_logging.assert_any_call("Server error: Simulated error")

# def test_client_handler_called(mock_valid_configuration):
#     """Test that the client handler function is called correctly when a client connects."""
#     with mock.patch("socket.socket") as mock_socket:
#         with mock.patch("threading.Thread") as mock_thread:
#             mock_socket.return_value.accept.return_value = ("client_socket", ("127.0.0.1", 12345))
#             with mock.patch("your_module.client_handler.handle_client") as mock_handle_client:
#                 start_server()  # Call the function to start the server

#                 # Ensure that the handle_client function is called with the correct arguments
#                 mock_handle_client.assert_called_once_with(
#                     "client_socket", ("127.0.0.1", 12345), FILE_PATH, REREAD_ON_QUERY, []
#                 )

# @pytest.fixture
# def mock_reread_false(monkeypatch):
#     """Mock REREAD_ON_QUERY to be False."""
#     monkeypatch.setenv("REREAD_ON_QUERY", "false")
#     monkeypatch.setenv("FILE_PATH", "/valid/path/to/file")

# def test_load_file_into_cache(mock_reread_false):
#     """Test that the file is loaded into cache when reread_on_query is False."""
#     with mock.patch("your_module.file_utils.load_file_into_cache") as mock_load_file:
#         start_server()  # Call the function to start the server

#         # Ensure that the file is loaded into cache
#         mock_load_file.assert_called_once_with("/valid/path/to/file")

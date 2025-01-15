# import pytest
# from unittest.mock import Mock, patch
# from py_server.client_handler import handle_client, log_performance_metrics


# @pytest.fixture
# def mock_socket():
#     """Fixture to provide a mock socket object."""
#     return Mock()


# @pytest.fixture
# def mock_client_address():
#     """Fixture to provide a mock client address."""
#     return ("127.0.0.1", 8080)


# @pytest.fixture
# def mock_cached_lines():
#     """Fixture to provide a mock cached lines list."""
#     return ["This is a sample line.", "Another sample line."]


# def test_log_performance_metrics(mocker):
#     """Test log_performance_metrics function logs expected metrics."""
#     mock_logging = mocker.patch("py_server.client_handler.logging.info")

#     log_performance_metrics(
#         search_function_name="linux_grep_search",
#         file_path="test_file.txt",
#         reread_option=True,
#         elapsed_time=0.123456,
#         memory_usage=5.6789,
#         client_address=("192.168.0.1", 12345),
#     )

#     mock_logging.assert_called_once_with(
#         "Performance Metrics: Function=linux_grep_search, FilePath=test_file.txt, "
#         "RereadOption=True, ElapsedTime=0.123456 seconds, MemoryUsage=5.678900 MB, "
#         "ClientAddress=('192.168.0.1', 12345)"
#     )


# def test_handle_client_no_data(mock_socket, mock_client_address):
#     """Test handle_client when no data is received."""
#     client_socket = mock_socket
#     client_socket.recv.return_value = b""

#     handle_client(client_socket, mock_client_address, "test_file.txt", False)

#     client_socket.recv.assert_called_once_with(1024)
#     client_socket.close.assert_called_once()


# def test_handle_client_empty_message(mock_socket, mock_client_address):
#     """Test handle_client when an empty message is received."""
#     client_socket = mock_socket
#     client_socket.recv.return_value = b"\x00"

#     handle_client(client_socket, mock_client_address, "test_file.txt", False)

#     client_socket.recv.assert_called_once_with(1024)
#     client_socket.close.assert_called_once()


# def test_handle_client_missing_file_path(mock_socket, mock_client_address):
#     """Test handle_client when the file path is missing."""
#     client_socket = mock_socket
#     client_socket.recv.return_value = b"Test Message"

#     handle_client(client_socket, mock_client_address, None, False)

#     client_socket.send.assert_called_once_with(b"Error: File path not configured properly.\n")
#     client_socket.close.assert_called_once()


# @pytest.mark.parametrize(
#     "search_result, expected_response",
#     [
#         (True, b"STRING EXISTS\n"),
#         (False, b"STRING NOT FOUND\n"),
#         (None, b"Error: Unable to search the file.\n"),
#     ],
# )
# def test_handle_client_search_results(
#     mock_socket, mock_client_address, search_result, expected_response, mock_cached_lines
# ):
#     """Test handle_client with various search results."""
#     client_socket = mock_socket
#     client_socket.recv.return_value = b"Test Query"

#     with patch("py_server.file_utiils.linux_grep_search") as mock_search:
#         mock_search.return_value = search_result

#         handle_client(client_socket, mock_client_address, "test_file.txt", True, mock_cached_lines)

#         client_socket.send.assert_called_once_with(expected_response)
#         client_socket.close.assert_called_once()


# def test_handle_client_performance_metrics(mock_socket, mock_client_address, mock_cached_lines):
#     """Test handle_client logs performance metrics correctly."""
#     client_socket = mock_socket
#     client_socket.recv.return_value = b"Test Query"

#     with patch("py_server.file_utiils.linux_grep_search", return_value=True), \
#          patch("py_server.client_handler.log_performance_metrics") as mock_log_metrics:

#         handle_client(client_socket, mock_client_address, "test_file.txt", True, mock_cached_lines)

#         mock_log_metrics.assert_called_once()
#         client_socket.close.assert_called_once()


# def test_handle_client_exception_handling(mock_socket, mock_client_address):
#     """Test handle_client handles exceptions gracefully."""
#     client_socket = mock_socket
#     client_socket.recv.side_effect = Exception("Mock exception")

#     handle_client(client_socket, mock_client_address, "test_file.txt", False)

#     client_socket.close.assert_called_once()


# def test_handle_client_reread_disabled(mock_socket, mock_client_address, mock_cached_lines):
#     """Test handle_client with reread_on_query disabled."""
#     client_socket = mock_socket
#     client_socket.recv.return_value = b"Cached Query"

#     with patch("py_server.file_utiils.linux_grep_search") as mock_search:
#         mock_search.return_value = True

#         handle_client(client_socket, mock_client_address, "test_file.txt", False, mock_cached_lines)

#         mock_search.assert_called_once_with(
#             "test_file.txt", "Cached Query", False, mock_cached_lines
#         )
#         client_socket.send.assert_called_once_with(b"STRING EXISTS\n")
#         client_socket.close.assert_called_once()

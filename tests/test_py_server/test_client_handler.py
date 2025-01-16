import pytest
from unittest.mock import MagicMock, patch
from py_server.client_handler import log_performance_metrics
from py_server.client_handler import handle_client


def test_log_performance_metrics_valid_input():
    """
    Test that `log_performance_metrics` logs the correct message.
    """
    with patch("py_server.client_handler.logging.info") as mock_log:
        log_performance_metrics(
            search_function_name="linux_grep_search",
            file_path="/path/to/file.txt",
            reread_option=True,
            elapsed_time=1.234567,
            memory_usage=12.345678,
            client_address=("127.0.0.1", 12345),
        )
        mock_log.assert_called_once_with(
            "Performance Metrics: Function=linux_grep_search, "
            "FilePath=/path/to/file.txt, RereadOption=True, "
            "ElapsedTime=1.234567 seconds,"
            "MemoryUsage=12.345678 MB,"
            "ClientAddress=('127.0.0.1', 12345)"
        )


def test_log_performance_metrics_missing_file_path():
    """
    Test `log_performance_metrics` with a missing file path.
    """
    with patch("py_server.client_handler.logging.info") as mock_log:
        log_performance_metrics(
            search_function_name="linux_grep_search",
            file_path=None,
            reread_option=False,
            elapsed_time=0.56789,
            memory_usage=8.9101112,
            client_address=("192.168.0.1", 54321),
        )
        mock_log.assert_called_once_with(
            "Performance Metrics: Function=linux_grep_search, "
            "FilePath=None, RereadOption=False, "
            "ElapsedTime=0.567890 seconds,"
            "MemoryUsage=8.910111 MB,"
            "ClientAddress=('192.168.0.1', 54321)"
        )


@pytest.fixture
def mock_client_socket():
    """
    Fixture to provide a mock client socket.
    """
    client_socket = MagicMock()
    return client_socket


def test_handle_client_valid_message(mock_client_socket):
    """
    Test `handle_client` with a valid message and file path.
    """
    mock_client_socket.recv.side_effect = [b"test_message\x00", b""]
    with patch(
        "py_server.client_handler.linux_grep_search", return_value=True
    ):
        with patch("py_server.client_handler.log_performance_metrics"):
            handle_client(
                client_socket=mock_client_socket,
                client_address=("127.0.0.1", 12345),
                file_path="/path/to/file.txt",
                reread_on_query=True,
                cached_lines=None,
            )
            mock_client_socket.close.assert_called_once()


def test_handle_client_empty_message(mock_client_socket):
    """
    Test `handle_client` with an empty message.
    """
    mock_client_socket.recv.side_effect = [b"\x00", b""]
    handle_client(
        client_socket=mock_client_socket,
        client_address=("127.0.0.1", 12345),
        file_path="/path/to/file.txt",
        reread_on_query=True,
        cached_lines=None,
    )
    mock_client_socket.close.assert_called_once()


def test_handle_client_no_file_path(mock_client_socket):
    """
    Test `handle_client` when file_path is not provided.
    """
    mock_client_socket.recv.side_effect = [b"test_message\x00", b""]
    handle_client(
        client_socket=mock_client_socket,
        client_address=("127.0.0.1", 12345),
        file_path=None,
        reread_on_query=True,
        cached_lines=None,
    )
    mock_client_socket.send.assert_called_with(
        b"Error: File path not configured properly.\n"
    )
    mock_client_socket.close.assert_called_once()


def test_handle_client_search_error(mock_client_socket):
    """
    Test `handle_client` when `linux_grep_search` raises an exception.
    """
    mock_client_socket.recv.side_effect = [b"test_message\x00", b""]
    with patch(
        "py_server.client_handler.linux_grep_search",
        side_effect=Exception("Search failed")
    ):
        handle_client(
            client_socket=mock_client_socket,
            client_address=("127.0.0.1", 12345),
            file_path="/path/to/file.txt",
            reread_on_query=True,
            cached_lines=None,
        )
        mock_client_socket.close.assert_called_once()


def test_handle_client_disconnect_on_no_data(mock_client_socket):
    """
    Test `handle_client` when the client sends no data.
    """
    mock_client_socket.recv.return_value = b""
    handle_client(
        client_socket=mock_client_socket,
        client_address=("127.0.0.1", 12345),
        file_path="/path/to/file.txt",
        reread_on_query=False,
        cached_lines=None,
    )
    mock_client_socket.close.assert_called_once()

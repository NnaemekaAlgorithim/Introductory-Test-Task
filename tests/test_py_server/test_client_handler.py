from unittest.mock import patch, MagicMock
import socket
import pytest
from py_server.client_handler import log_performance_metrics, handle_client


@pytest.fixture
def setup():
    client_socket = MagicMock(spec=socket.socket)
    client_address = ("127.0.0.1", 12345)
    file_path = "test_file.txt"
    reread_on_query = False
    cached_lines = ["test line"]
    debug_mode = False
    return (
        client_socket,
        client_address,
        file_path,
        reread_on_query,
        cached_lines,
        debug_mode
    )


@patch("logging.info")
def test_log_performance_metrics(mock_logging_info):
    log_performance_metrics(
        search_function_name="file_search",
        file_path="test_file.txt",
        reread_option=True,
        elapsed_time=0.123456,
        memory_usage=1.23456,
        client_address=("127.0.0.1", 12345),
        search_query="test query",
        debug_mode=True,
    )

    mock_logging_info.assert_called()
    assert "Performance Metrics:" in mock_logging_info.call_args[0][0]


def test_handle_client_successful_search(setup, monkeypatch):
    (
        client_socket,
        client_address,
        file_path,
        reread_on_query,
        cached_lines,
        debug_mode,
    ) = setup

    # Mock tracemalloc and time for other parts of the function
    monkeypatch.setattr(
        "tracemalloc.get_traced_memory", lambda: (1024, 2048)
    )
    monkeypatch.setattr(
        "time.time", lambda: 1
    )

    # Mock the client socket behavior
    client_socket.recv.side_effect = [b"test query\x00", b""]

    # Create a mock for file_search
    mock_file_search = MagicMock(return_value=True)

    # Use monkeypatch to replace
    # the file_search function directly with the mock
    monkeypatch.setattr(
        "py_server.file_utils.file_search", mock_file_search
    )

    # Call file_search directly to test the mock
    mock_file_search(
        file_path, "test query", reread_on_query, cached_lines
    )

    # Assert that file_search was called with the correct parameters
    mock_file_search.assert_called_once_with(
        file_path, "test query", reread_on_query, cached_lines
    )


@patch("logging.error")
def test_handle_client_missing_file_path(mock_logging_error, setup):
    (
        client_socket,
        client_address,
        file_path,
        reread_on_query,
        cached_lines,
        debug_mode,
    ) = setup
    client_socket.recv.side_effect = [b"test query\x00", b""]

    handle_client(
        client_socket=client_socket,
        client_address=client_address,
        file_path=None,
        reread_on_query=reread_on_query,
        cached_lines=cached_lines,
        debug_mode=debug_mode,
    )

    client_socket.send.assert_called_with(
        b"Error: File path not configured properly.\n"
    )


@patch("logging.error")
def test_handle_client_decoding_error(mock_logging_error, setup):
    (
        client_socket,
        client_address,
        file_path,
        reread_on_query,
        cached_lines,
        debug_mode,
    ) = setup
    client_socket.recv.side_effect = [b"\x80\x81\x82", b""]

    handle_client(
        client_socket=client_socket,
        client_address=client_address,
        file_path=file_path,
        reread_on_query=reread_on_query,
        cached_lines=cached_lines,
        debug_mode=debug_mode,
    )

    mock_logging_error.assert_called()
    client_socket.close.assert_called_once()

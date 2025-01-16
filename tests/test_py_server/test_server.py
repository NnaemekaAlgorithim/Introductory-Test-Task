from dotenv import load_dotenv
import pytest
import ssl
from unittest.mock import patch, MagicMock

from py_server.server import (
    get_file_path_and_reread_option,
    create_ssl_context,
    start_server,
    run_as_daemon,
    run_locally,
)
from py_server.config import (
    FILE_PATH,
    REREAD_ON_QUERY
)


# Mock configuration values
@pytest.fixture(autouse=True)
def mock_config(monkeypatch):
    monkeypatch.setattr("py_server.config.FILE_PATH", "/test/path")
    monkeypatch.setattr("py_server.config.REREAD_ON_QUERY", False)
    monkeypatch.setattr("py_server.config.SSL_CERTIFICATE", "/path/cert.pem")
    monkeypatch.setattr("py_server.config.SSL_KEY", "/path/to/key.pem")
    monkeypatch.setattr("py_server.config.ENABLE_SSL", True)
    monkeypatch.setattr("py_server.config.HOST", "127.0.0.1")
    monkeypatch.setattr("py_server.config.PORT", 5000)


# Load .env file
load_dotenv()


def test_get_file_path_and_reread_option():
    """
    Test that the function retrieves the correct file path and reread option.
    """
    expected_file_path = FILE_PATH
    expected_reread_on_query = REREAD_ON_QUERY

    file_path, reread_on_query = get_file_path_and_reread_option()

    assert file_path == expected_file_path
    assert reread_on_query == expected_reread_on_query


def test_create_ssl_context():
    """
    Test SSL context creation and configuration.
    """
    ssl_context = create_ssl_context()
    assert isinstance(ssl_context, ssl.SSLContext)
    assert ssl_context.protocol == ssl.PROTOCOL_TLS_SERVER
    assert ssl.OP_NO_TLSv1 in ssl_context.options
    assert ssl.OP_NO_TLSv1_1 in ssl_context.options


@patch("py_server.server.socket.socket")
def test_start_server(mock_socket):
    """
    Test server start with mock socket.
    """
    # Mock the server socket
    mock_server_socket = MagicMock()
    mock_socket.return_value = mock_server_socket

    # Mock dependent functions and methods
    with patch(
        "py_server.file_utils.load_file_into_cache",
        return_value=["Line1", "Line2"]
        ), \
            patch("py_server.client_handler.handle_client"):

        # Simulate server accepting a connection and
        # then stopping on KeyboardInterrupt
        mock_server_socket.accept.side_effect = [
            (MagicMock(), ("127.0.0.1", 12345)),
            KeyboardInterrupt,  # Simulate server shutdown
        ]

        # Call the function under test
        start_server()


@patch("py_server.server.threading.Thread")
def test_start_server_with_threads(mock_thread):
    """
    Test server threading for client handling.
    """
    mock_client_socket = MagicMock()
    mock_client_address = ("127.0.0.1", 12345)
    mock_server_socket = MagicMock()
    mock_server_socket.accept.side_effect = [
        (mock_client_socket, mock_client_address), KeyboardInterrupt
    ]

    with patch(
        "py_server.server.socket.socket",
        return_value=mock_server_socket
    ), \
            patch(
                "py_server.file_utils.load_file_into_cache",
                return_value=[]
            ):
        start_server()


@patch("py_server.server.daemon.DaemonContext")
@patch("py_server.server.socket.socket")
def test_run_as_daemon(mock_socket, mock_daemon_context):
    """
    Test that the server runs in daemon mode without
    actually binding to a port.
    """
    # Mock the socket to avoid binding to the port
    mock_socket_instance = MagicMock()
    mock_socket.return_value = mock_socket_instance
    mock_socket_instance.bind.return_value = None

    # Ensure DaemonContext does not block the test
    mock_daemon_instance = MagicMock()
    mock_daemon_context.return_value = mock_daemon_instance

    # Call the function under test
    run_as_daemon()

    # Verify DaemonContext was used as expected
    mock_daemon_context.assert_called_once()


@patch("py_server.server.start_server")
def test_run_locally(mock_start_server):
    """
    Test that the server runs locally.
    """
    run_locally()
    mock_start_server.assert_called_once()


def test_main_run_locally():
    """
    Test the main function when running locally.
    """
    pass


def test_main_run_as_daemon():
    """
    Test the main function when running as a daemon.
    """
    pass

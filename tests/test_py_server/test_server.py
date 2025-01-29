import os
import pytest
import socket
import ssl
from unittest.mock import patch
from py_server.config import FILE_PATH, REREAD_ON_QUERY
from py_server.server import (
    get_file_path_and_reread_option,
    create_ssl_context,
    start_server,
    run_as_daemon,
    run_locally,
)


@pytest.fixture(scope="class")
def mock_config():
    """Fixture to mock configuration variables."""
    with patch("py_server.config.FILE_PATH", "/mock/path/to/file"), \
         patch("py_server.config.REREAD_ON_QUERY", False), \
         patch("py_server.config.SSL_CERTIFICATE", "/mock/path/to/cert.pem"), \
         patch("py_server.config.SSL_KEY", "/mock/path/to/key.pem"), \
         patch("py_server.config.ENABLE_SSL", True):
        yield


def test_get_file_path_and_reread_option(mock_config):
    """Test retrieval of file path and reread option."""
    file_path, reread_option = get_file_path_and_reread_option()
    assert file_path == FILE_PATH
    assert reread_option == REREAD_ON_QUERY


def test_create_ssl_context_success(mock_config):
    """Test successful creation of an SSL context."""
    ssl_context = create_ssl_context()
    assert isinstance(ssl_context, ssl.SSLContext)
    assert ssl_context.options & ssl.OP_NO_TLSv1
    assert ssl_context.options & ssl.OP_NO_TLSv1_1


def test_create_ssl_context_file_not_found():
    """Test SSL context creation with missing certificate or key."""
    mock_env = {'SSL_CERTIFICATE': '/invalid/path', 'SSL_KEY': '/invalid/key'}
    with patch.dict(os.environ, mock_env), \
         patch.object(
             ssl.SSLContext, 'load_cert_chain', side_effect=FileNotFoundError
         ):
        with pytest.raises(FileNotFoundError):
            create_ssl_context()


def test_create_ssl_context_ssl_error():
    """Test SSL context creation with SSL configuration error."""
    with patch(
        "ssl.SSLContext.load_cert_chain",
        side_effect=ssl.SSLError("SSL error")
    ), pytest.raises(ssl.SSLError):
        create_ssl_context()


def test_start_server_no_file_path(mock_config):
    """Test server startup without a valid file path."""
    with patch(
        "py_server.server.get_file_path_and_reread_option",
        return_value=("", False)
    ), patch("logging.error") as mock_log:
        start_server()
        mock_log.assert_called_with(
            "Server cannot start without a valid file path."
        )


def test_start_server_file_not_found(mock_config):
    """Test server startup with missing file."""
    with patch(
        "py_server.file_utils.load_file_into_cache",
        side_effect=FileNotFoundError
    ), patch("logging.error") as mock_error, patch(
        "socket.socket",
        side_effect=socket.error("File not found")
    ):
        try:
            start_server()
        except KeyboardInterrupt:
            pass  # Gracefully handle keyboard interrupt

    # Assert expected logging error
    assert mock_error.called, "Expected logging error about missing file"
    assert "File not found" in mock_error.call_args[0][0], (
        "Wrong error message logged"
    )


def test_run_as_daemon(mock_config):
    """Test running the server as a daemon."""
    with patch("py_server.server.start_server"), \
         patch("daemon.DaemonContext") as mock_daemon:
        run_as_daemon()
        mock_daemon.assert_called_once()


def test_run_locally(mock_config):
    """Test running the server locally."""
    with patch("py_server.server.start_server") as mock_start_server:
        run_locally()
        mock_start_server.assert_called_once()


def test_socket_error_handling(mock_config):
    """Test server startup with socket error handling."""
    with patch("socket.socket") as mock_socket:
        mock_socket.side_effect = OSError("Socket error")
        with patch("logging.error") as mock_log:
            start_server()
            mock_log.assert_called_with("Socket error: Socket error")

import logging
import socket
import ssl
import threading
import sys
from typing import List, Tuple
import daemon
from py_server.config import HOST, PORT, FILE_PATH, REREAD_ON_QUERY
from py_server.config import SSL_CERTIFICATE, MAX_BUFFER_SIZE
from py_server.config import SSL_KEY, ENABLE_SSL
from py_server.file_utils import load_file_into_cache
from py_server.client_handler import handle_client


def get_file_path_and_reread_option() -> Tuple[str, bool]:
    """
    Retrieve the file path and the REREAD_ON_QUERY option from the configuration.

    Returns:
        Tuple[str, bool]: File path as a string and reread option as a boolean.
    """
    file_path: str = FILE_PATH
    reread_on_query: bool = REREAD_ON_QUERY
    return file_path, reread_on_query


def create_ssl_context() -> ssl.SSLContext:
    """
    Create and configure an SSL context for secure communication.

    Returns:
        ssl.SSLContext: Configured SSL context.
    """
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile=SSL_CERTIFICATE, keyfile=SSL_KEY)
    ssl_context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # Disable weak protocols
    return ssl_context


def start_server() -> None:
    """
    Start the server to handle multiple client connections.

    This function initializes the server socket, retrieves the file path
    and reread option, and handles incoming client connections in separate threads.
    """
    file_path, reread_on_query = get_file_path_and_reread_option()

    if not file_path:
        logging.error("Server cannot start without a valid file path.")
        return

    cached_lines: List[str] = []
    if not reread_on_query:
        cached_lines = load_file_into_cache(file_path)

    # Create server socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        logging.info(f"Server started on {HOST}:{PORT}")

        if ENABLE_SSL:
            ssl_context = create_ssl_context()
            server_socket = ssl_context.wrap_socket(server_socket, server_side=True)
            logging.info("SSL enabled. Using secure connection.")

        try:
            while True:
                client_socket, client_address = server_socket.accept()
                logging.info(f"Connection accepted from {client_address}")

                # Wrap client socket with SSL if enabled
                if ENABLE_SSL:
                    try:
                        client_socket = ssl_context.wrap_socket(client_socket, server_side=True)
                    except ssl.SSLError as e:
                        logging.warning(f"SSL error with client {client_address}: {e}")
                        client_socket.close()
                        continue

                client_thread = threading.Thread(
                    target=handle_client,
                    args=(client_socket, client_address, file_path, reread_on_query, cached_lines)
                )
                client_thread.daemon = True
                client_thread.start()
        except KeyboardInterrupt:
            logging.info("Server shutting down gracefully...")
        except Exception as error:
            logging.error(f"Server encountered an error: {error}")
        finally:
            logging.info("Server socket closed.")


def run_as_daemon() -> None:
    """
    Run the server in daemon mode, detached from the terminal.
    """
    with daemon.DaemonContext():
        start_server()


def run_locally() -> None:
    """
    Run the server locally, allowing it to interact with the terminal.
    """
    start_server()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "daemon":
        logging.info("Running as a daemon...")
        run_as_daemon()
    else:
        logging.info("Running locally...")
        run_locally()

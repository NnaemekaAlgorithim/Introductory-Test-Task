import logging
import socket
import ssl
import threading
import sys
from typing import List, Tuple
import daemon
from py_server.config import (
    HOST,
    PORT,
    FILE_PATH,
    REREAD_ON_QUERY,
    SSL_CERTIFICATE,
    SSL_KEY,
    ENABLE_SSL,
    LOG_FILE,
    DEBUG,
    validate_config,
)
from py_server.file_utils import load_file_into_cache
from py_server.client_handler import handle_client


"""
Server Module

This module defines the functionality to start and manage
a server for handling client connections. It includes:

- `get_file_path_and_reread_option`:Retrieves the file path and
reread option from the configuration.

- `create_ssl_context`: Configures an SSL context for
secure communication if SSL is enabled.

- `start_server`: Initializes and starts the server,
handling client connections and
optionally wrapping them with SSL.

- `run_as_daemon`: Runs the server in daemon mode,
detached from the terminal.

- `run_locally`: Runs the server in local mode,
allowing terminal interaction.

The module integrates with the configuration, logging, and
utility components to ensure proper server setup and operation.
"""


def get_file_path_and_reread_option() -> Tuple[str, bool]:
    """
    Retrieve the file path and the REREAD_ON_QUERY option
    from the configuration.

    Returns:
    Tuple[str, bool]: File path as a string and reread
    option as a boolean.
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
    try:
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(certfile=SSL_CERTIFICATE, keyfile=SSL_KEY)
        ssl_context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
        return ssl_context
    except FileNotFoundError:
        logging.error(
            f"SSL certificate or key file not found:"
            f"{SSL_CERTIFICATE}, {SSL_KEY}"
        )
        raise
    except ssl.SSLError as e:
        logging.error(
            f"SSL configuration error: {e}"
        )
        raise
    except Exception as e:
        logging.error(
            f"Unexpected error while creating SSL context: {e}"
        )
        raise


def start_server() -> None:
    """
    Start the server to handle multiple client connections.

    Initializes the server socket, retrieves the file path and reread option,
    and handles incoming client connections in separate threads.
    """
    file_path, reread_on_query = get_file_path_and_reread_option()

    if not file_path:
        logging.error(
            "Server cannot start without a valid file path."
        )
        return

    cached_lines: List[str] = []
    if not reread_on_query:
        try:
            cached_lines = load_file_into_cache(file_path)
        except FileNotFoundError:
            logging.error(
                f"File not found: {file_path}"
            )
            return
        except PermissionError:
            logging.error(
                f"Permission denied for file: {file_path}"
            )
            return
        except Exception as e:
            logging.error(
                f"Unexpected error while loading file: {e}"
            )
            return

    # Create server socket
    try:
        with socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        ) as server_socket:
            server_socket.setsockopt(
                socket.SOL_SOCKET, socket.SO_REUSEADDR, 1
            )
            server_socket.bind((HOST, PORT))
            server_socket.listen()
            logging.info(
                f"Server started on {HOST}:{PORT}"
            )

            ssl_context = None
            if ENABLE_SSL:
                ssl_context = create_ssl_context()
                logging.info(
                    "SSL enabled. Using secure connection."
                )

            try:
                while True:
                    try:
                        client_socket, client_address = server_socket.accept()
                        logging.info(
                            f"Connection accepted from {client_address}"
                        )
                    except socket.error as e:
                        logging.error(
                            f"Error accepting connection: {e}"
                        )
                        continue

                    # Wrap client socket with SSL if enabled
                    if ENABLE_SSL and ssl_context:
                        try:
                            client_socket = ssl_context.wrap_socket(
                                client_socket, server_side=True
                            )
                        except ssl.SSLError as e:
                            logging.warning(
                                f"SSL handshake failed with"
                                f"{client_address}: {e}"
                            )
                            client_socket.close()
                            continue
                        except Exception as e:
                            logging.error(
                                f"Unexpected error during SSL wrapping: {e}"
                            )
                            client_socket.close()
                            continue

                    client_thread = threading.Thread(
                        target=handle_client,
                        args=(
                            client_socket,
                            client_address,
                            file_path,
                            reread_on_query,
                            cached_lines,
                            DEBUG,
                        ),
                        daemon=True,
                    )
                    client_thread.start()
            except KeyboardInterrupt:
                logging.info(
                    "Server shutting down gracefully..."
                )
                sys.exit(0)
            except MemoryError:
                logging.critical(
                    "Memory error: Insufficient resources to continue."
                )
                sys.exit(1)
            except Exception as error:
                logging.error(
                    f"Server encountered an error: {error}", exc_info=True
                )
            finally:
                logging.info(
                    "Server socket closed."
                )
    except OSError as e:
        logging.error(
            f"Socket error: {e}"
        )
    except Exception as e:
        logging.error(
            f"Unexpected error during server setup: {e}"
        )


def run_as_daemon() -> None:
    """
    Run the server in daemon mode, detached from the terminal.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(LOG_FILE)],
    )
    with daemon.DaemonContext():
        try:
            start_server()
        except Exception as e:
            logging.error(
                f"Error running server in daemon mode: {e}", exc_info=True
            )


def run_locally() -> None:
    """
    Run the server locally, allowing it to interact with the terminal.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE), logging.StreamHandler(sys.stdout)
        ],
    )
    start_server()


if __name__ == "__main__":
    try:
        validate_config()
        print("Configuration validated successfully.")
    except ValueError as error:
        logging.critical(
            f"Configuration validation failed: {error}"
        )
        sys.exit(1)

    if len(sys.argv) > 1 and sys.argv[1] == "daemon":
        logging.info(
            "Running as a daemon..."
        )
        run_as_daemon()
    else:
        logging.info(
            "Running locally..."
        )
        run_locally()

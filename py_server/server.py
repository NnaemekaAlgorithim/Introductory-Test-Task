import logging
import socket
import threading
from config import HOST, PORT, env_file_path, env_reread_on_query
from logging_config import configure_logging
from file_utils import load_file_into_cache
from client_handler import handle_client

# Initialize logging configuration
configure_logging()

def get_file_path_and_reread_option():
    """Retrieve the file path and REREAD_ON_QUERY option from the configuration."""
    file_path = env_file_path
    reread_on_query = env_reread_on_query
    return file_path, reread_on_query

def start_server():
    """Start the server to handle multiple client connections."""
    file_path, reread_on_query = get_file_path_and_reread_option()
    if not file_path:
        logging.error("Server cannot start without a valid file path.")
        return

    cached_lines = []
    if not reread_on_query:
        cached_lines = load_file_into_cache(file_path)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    logging.info(f"Server started on {HOST}:{PORT}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address, file_path, reread_on_query, cached_lines)
            )
            client_thread.daemon = True
            client_thread.start()
    except KeyboardInterrupt:
        logging.info("Server shutting down...")
    except Exception as e:
        logging.error(f"Server error: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()

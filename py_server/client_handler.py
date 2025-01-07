import logging
from file_utils import search_in_file

def handle_client(client_socket, client_address, file_path, reread_on_query, cached_lines=None):
    """Handle an individual client connection."""
    logging.info(f"Connection established with {client_address}")

    try:
        while True:
            data = client_socket.recv(1024)  # Adjust the buffer size if needed
            if not data:
                break

            message = data.rstrip(b'\x00').decode('utf-8').strip()
            logging.info(f"Received from {client_address}: {message}")

            if file_path:
                result = search_in_file(file_path, message, reread_on_query, cached_lines)
                if result is None:
                    response = "Error: Unable to search the file.\n"
                elif result:
                    response = "STRING EXISTS\n"
                else:
                    response = "STRING NOT FOUND\n"
            else:
                response = "Error: File path not configured properly.\n"

            client_socket.send(response.encode('utf-8'))

    except Exception as e:
        logging.error(f"Error handling client {client_address}: {e}")
    finally:
        client_socket.close()
        logging.info(f"Connection closed with {client_address}")

import socket
import ssl
import time
import tracemalloc
from typing import Tuple
import os
from dotenv import load_dotenv


# Load environment variables from the .env file
load_dotenv()

# Server configuration
HOST: str = os.getenv("HOST", "0.0.0.0")
PORT: int = int(os.getenv("PORT", 44445))
BUFFER_SIZE: int = int(os.getenv("BUFFER_SIZE", 1024))
CA_CERT_FILE: str = os.getenv("CA_CERT_FILE")


# Toggle SSL on or off
USE_SSL: bool = os.getenv("USE_SSL", "False").lower() == "true"
print(USE_SSL)


def measure_response_time_and_memory(
            host: str,
            port: int,
            message: str
        ) -> Tuple[str, float, float]:
    """
    Sends a message to the server (optionally over SSL) and
    measures response time and memory usage.

    Args:
        host (str): Server's IP address.
        port (int): Server's port number.
        message (str): Message to send to the server.

    Returns:
        Tuple[str, float, float]: Server's response,
        time taken in seconds, and peak memory usage in MB.
    """
    tracemalloc.start()  # Start tracking memory usage

    # Create a raw socket
    raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if USE_SSL:
        # Create an SSL context and disable
        # certificate verification (FOR DEVELOPMENT ONLY)
        context = ssl.create_default_context()
        context.check_hostname = False 
        context.verify_mode = ssl.CERT_NONE
        client_socket = context.wrap_socket(
            raw_socket, server_hostname=host
        )
        print(f"SSL is enabled. Using SSL to connect to {host}:{port}")
    else:
        # Use plain socket if SSL is disabled
        client_socket = raw_socket
        print(
            f"SSL is disabled. Using plain socket to connect to {host}:{port}"
        )

    with client_socket:
        try:
            # Connect to the server
            client_socket.connect((host, port))
            print(f"Connected to server at {host}:{port}")

            # Measure time to send message and receive response
            start_time: float = time.time()

            # Send the message
            client_socket.sendall(message.encode("utf-8"))
            print(f"Sent: {message}")

            # Receive the response
            response: str = client_socket.recv(BUFFER_SIZE).decode("utf-8")
            end_time: float = time.time()

            # Calculate elapsed time
            elapsed_time: float = end_time - start_time

            # Stop memory tracking and get peak memory usage
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            peak_memory_usage = peak / 1024 / 1024  # Convert to MB

            return response.strip(), elapsed_time, peak_memory_usage

        except (socket.error, Exception) as error:
            tracemalloc.stop()  # Stop memory tracking in case of error
            raise RuntimeError(
                f"An error occurred while"
                f"communicating with the server: {error}"
            )


def main() -> None:
    """
    Main function to handle user input and execute the client workflow.
    """
    print(
        f"{'SSL' if USE_SSL else 'Plain'}"
        f"Client for measuring server response times and memory usage."
    )
    message: str = input("Enter the message to send to the server: ")

    # Check if the message is empty
    if not message.strip():
        print("Empty message provided. Terminating connection.")
        return

    try:
        response, elapsed_time, memory_usage = (
            measure_response_time_and_memory(
                HOST,
                PORT,
                message
            )
        )

        # Display server's response, elapsed time, and memory usage
        print(f"Received: {response}")
        print(f"Time taken for response: {elapsed_time:.6f} seconds")
        print(f"Peak memory usage: {memory_usage:.6f} MB")

    except RuntimeError as error:
        print(error)


if __name__ == "__main__":
    main()

"""
User-friendly client script to send messages to a server.

This script allows users to send a message to a server and receive its response.
Designed for simplicity and ease of use, this client abstracts performance
measurement details to focus solely on communication.
"""

import socket
from typing import Optional


# Server configuration
HOST: str = "0.0.0.0"  # Server IP address
PORT: int = 44445       # Server port
BUFFER_SIZE: int = 1024  # Size of the buffer for receiving data


def send_message_to_server(host: str, port: int, message: str) -> Optional[str]:
    """
    Sends a message to the server and receives its response.

    Args:
        host (str): Server's IP address.
        port (int): Server's port number.
        message (str): Message to send to the server.

    Returns:
        Optional[str]: Server's response, or None if an error occurred.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            # Connect to the server
            client_socket.connect((host, port))
            print(f"Connected to server at {host}:{port}")

            # Send the message
            client_socket.sendall(message.encode("utf-8"))
            print(f"Sent: {message}")

            # Receive and return the server's response
            response: str = client_socket.recv(BUFFER_SIZE).decode("utf-8")
            return response.strip()

        except (socket.error, Exception) as error:
            print(f"An error occurred: {error}")
            return None


def main() -> None:
    """
    Main function to handle user input and execute the client workflow.
    """
    print("Welcome to the Client Application!")
    print("Send a message to the server and receive a response.")
    
    message: str = input("Enter the message to send to the server: ")

    # Check if the message is empty
    if not message.strip():
        print("Empty message provided. Terminating connection.")
        return

    response = send_message_to_server(HOST, PORT, message)

    if response:
        print(f"Server Response: {response}")
    else:
        print("Failed to receive a response from the server.")


if __name__ == "__main__":
    main()

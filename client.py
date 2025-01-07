import socket
import time

HOST = '0.0.0.0'  # Server IP address
PORT = 44445        # Server port
BUFFER_SIZE = 1024  # Buffer size for receiving data

def main():
    message = input("Enter the message to send to the server: ")
    
    # Create a socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            # Connect to the server
            client_socket.connect((HOST, PORT))
            print(f"Connected to server at {HOST}:{PORT}")

            # Measure time to send message and receive response
            start_time = time.time()
            
            # Send the message
            client_socket.sendall(message.encode('utf-8'))
            print(f"Sent: {message}")

            # Receive the response
            response = client_socket.recv(BUFFER_SIZE).decode('utf-8')
            end_time = time.time()
            
            # Print the server's response
            print(f"Received: {response.strip()}")

            # Calculate and display the time taken
            elapsed_time = end_time - start_time
            print(f"Time taken for response: {elapsed_time:.6f} seconds")

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

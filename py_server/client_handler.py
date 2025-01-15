import logging
import time
import tracemalloc
from typing import Optional, List
from file_utils import linux_grep_search

"""
Module to manage client connection.

This module provides functions to handle individual client connection.
"""


def log_performance_metrics(
    search_function_name: str,
    file_path: Optional[str],
    reread_option: bool,
    elapsed_time: float,
    memory_usage: float,
    client_address: tuple[str, int],
) -> None:
    """
    Log performance metrics including response time, memory usage, and context.

    Args:
        search_function_name (str): Name of the search function used.
        file_path (Optional[str]): Path to the file being used.
        reread_option (bool): Whether the reread option is enabled.
        elapsed_time (float): Time taken for the operation in seconds.
        memory_usage (float): Peak memory usage in MB.
        client_address (tuple[str, int]): The client's IP address and port.
    """
    logging.info(
        f"Performance Metrics: Function={search_function_name}, "
        f"FilePath={file_path}, RereadOption={reread_option}, "
        f"ElapsedTime={elapsed_time:.6f} seconds, MemoryUsage={memory_usage:.6f} MB, "
        f"ClientAddress={client_address}"
    )


def handle_client(
    client_socket,
    client_address: tuple[str, int],
    file_path: Optional[str],
    reread_on_query: bool,
    cached_lines: Optional[List[str]] = None,
) -> None:
    """
    Handle an individual client connection.

    Args:
        client_socket: The socket object for the client connection.
        client_address (tuple[str, int]): tuple of client's IP address & port.
        file_path (Optional[str]): Path to the file to search in.
        reread_on_query (bool): Whether to reread the file on every query.
        cached_lines (Optional[List[str]]): Cached lines of the file, if any.

    Returns:
        None
    """
    logging.info(f"Connection established with {client_address}")

    try:
        while True:
            # Receive data from the client
            data = client_socket.recv(1024)
            if not data:
                logging.info(f"No data received from {client_address}. Closing connection.")
                break

            # Decode and clean up the received message
            message = data.rstrip(b"\x00").decode("utf-8").strip()
            
            if not message:
                logging.info(f"Empty message received from {client_address}. Closing connection.")
                break  # Gracefully handle empty message by ending the loop.

            logging.info(f"Received from {client_address}: {message}")

            # Process the search request
            if file_path:
                # Measure performance
                tracemalloc.start()
                start_time = time.time()
                
                search_function = linux_grep_search
                result = linux_grep_search(file_path, message, reread_on_query, cached_lines)
                logging.info(f"Search result: {result}")

                end_time = time.time()
                current, peak_memory = tracemalloc.get_traced_memory()
                tracemalloc.stop()

                elapsed_time = end_time - start_time
                memory_usage = peak_memory / (1024 * 1024)  # Convert bytes to MB

                # Log performance metrics
                log_performance_metrics(
                    search_function_name=search_function.__name__,
                    file_path=file_path,
                    reread_option=reread_on_query,
                    elapsed_time=elapsed_time,
                    memory_usage=memory_usage,
                    client_address=client_address,
                )

                # Construct the response
                if result is None:
                    response = "Error: Unable to search the file.\n"
                elif result:
                    response = "STRING EXISTS\n"
                else:
                    response = "STRING NOT FOUND\n"
            else:
                response = "Error: File path not configured properly.\n"

            # Send the response back to the client
            client_socket.send(response.encode("utf-8"))

    except Exception as e:
        logging.error(f"Error handling client {client_address}: {e}")
    finally:
        client_socket.close()
        logging.info(f"Connection closed with {client_address}")


# This code was used for handling client while testing many algorithms.
# import logging
# import time
# import tracemalloc
# from typing import Optional, List
# from .file_utils import search_line_by_line, regex_search, binary_search_sorted, in_memory_set_lookup, linux_grep_search, multithreaded_search, memory_mapped_search

# """
# Module to manage client connection.

# This module provides functions to handle individual client connection.
# """

# def log_performance_metrics(
#     search_function_name: str,
#     file_path: Optional[str],
#     reread_option: bool,
#     elapsed_time: float,
#     memory_usage: float,
#     client_address: tuple[str, int],
# ) -> None:
#     """
#     Log performance metrics including response time, memory usage, and context.

#     Args:
#         search_function_name (str): Name of the search function used.
#         file_path (Optional[str]): Path to the file being used.
#         reread_option (bool): Whether the reread option is enabled.
#         elapsed_time (float): Time taken for the operation in seconds.
#         memory_usage (float): Peak memory usage in MB.
#         client_address (tuple[str, int]): The client's IP address and port.
#     """
#     logging.info(
#         f"Performance Metrics: Function={search_function_name}, "
#         f"FilePath={file_path}, RereadOption={reread_option}, "
#         f"ElapsedTime={elapsed_time:.6f} seconds, MemoryUsage={memory_usage:.6f} MB, "
#         f"ClientAddress={client_address}"
#     )


# def handle_client(
#     client_socket,
#     client_address: tuple[str, int],
#     file_path: Optional[str],
#     reread_on_query: bool,
#     cached_lines: Optional[List[str]] = None,
# ) -> None:
#     """
#     Handle an individual client connection.

#     Args:
#         client_socket: The socket object for the client connection.
#         client_address (tuple[str, int]): tuple of client's IP address & port.
#         file_path (Optional[str]): Path to the file to search in.
#         reread_on_query (bool): Whether to reread the file on every query.
#         cached_lines (Optional[List[str]]): Cached lines of the file, if any.

#     Returns:
#         None
#     """
#     logging.info(f"Connection established with {client_address}")

#     try:
#         while True:
#             # Receive data from the client
#             data = client_socket.recv(1024)
#             if not data:
#                 logging.info(f"No data received from {client_address}. Closing connection.")
#                 break

#             # Decode and clean up the received message
#             message = data.rstrip(b"\x00").decode("utf-8").strip()
            
#             if not message:
#                 logging.info(f"Empty message received from {client_address}. Closing connection.")
#                 break  # Gracefully handle empty message by ending the loop.

#             logging.info(f"Received from {client_address}: {message}")

#             # Process the search request
#             if file_path:
#                 # Initialize search functions
#                 search_functions = [
#                     search_line_by_line,
#                     regex_search,
#                     binary_search_sorted,
#                     in_memory_set_lookup,
#                     linux_grep_search,
#                     multithreaded_search,
#                     memory_mapped_search,
#                 ]
                
#                 results = []
                
#                 for search_function in search_functions:
#                     # Measure performance for each search function
#                     tracemalloc.start()
#                     start_time = time.time()
                    
#                     result = search_function(file_path, message, reread_on_query, cached_lines)
                    
#                     end_time = time.time()
#                     current, peak_memory = tracemalloc.get_traced_memory()
#                     tracemalloc.stop()

#                     elapsed_time = end_time - start_time
#                     memory_usage = peak_memory / (1024 * 1024)  # Convert bytes to MB

#                     # Log performance metrics for each function
#                     log_performance_metrics(
#                         search_function_name=search_function.__name__,
#                         file_path=file_path,
#                         reread_option=reread_on_query,
#                         elapsed_time=elapsed_time,
#                         memory_usage=memory_usage,
#                         client_address=client_address,
#                     )
                    
#                     results.append((search_function.__name__, result))
                    
#                 # Construct the response
#                 response = ""
#                 for func_name, res in results:
#                     response += f"{func_name}: "
#                     if res is None:
#                         response += "Error: Unable to search the file.\n"
#                     elif res:
#                         response += "STRING EXISTS\n"
#                     else:
#                         response += "STRING NOT FOUND\n"
#             else:
#                 response = "Error: File path not configured properly.\n"

#             # Send the response back to the client
#             client_socket.send(response.encode("utf-8"))

#     except Exception as e:
#         logging.error(f"Error handling client {client_address}: {e}")
#     finally:
#         client_socket.close()
#         logging.info(f"Connection closed with {client_address}")

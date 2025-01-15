from bisect import bisect_left
from concurrent.futures import ThreadPoolExecutor
import logging
import mmap
import re
import subprocess
from typing import List, Optional, Union


"""
Function to manage client search request using Linux `grep`.

This function handles individual client search requests, leveraging the 
Linux `grep` command or a cached line-based search mechanism.
"""
def linux_grep_search(
    file_path: str,
    search_string: str,
    reread_on_query: bool,
    cached_lines: Optional[List[str]] = None,
) -> Union[bool, None]:
    """
    Search for an exact match of a string in a file using Linux `grep` or cached content.

    If `reread_on_query` is True, the function uses the Linux `grep` command to 
    directly search the file. Otherwise, it searches within the provided cached 
    lines.

    Args:
        file_path (str): Path to the file to search.
        search_string (str): The string to search for.
        reread_on_query (bool): Whether to reread the file using `grep` on each query.
        cached_lines (Optional[List[str]]): Cached lines of the file.

    Returns:
        bool: True if the string is found, False otherwise.
        None: If an error occurs (e.g., file not found or command failure).
    """
    try:
        if reread_on_query:
            # Use Linux `grep` to search the file directly
            result = subprocess.run(
                ["grep", "-Fxq", search_string, file_path],
                capture_output=True,
                text=True,
            )
            return result.returncode == 0
        elif cached_lines is not None:
            # Search within the cached lines
            return any(line.strip() == search_string for line in cached_lines)
        else:
            logging.warning("No cached lines provided for search.")
            return False
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return None
    except Exception as error:
        logging.error(f"Error in linux_grep_search: {error}")
        return None


#This set of codes was used for testing various algorithms.
# """
# Function to manage client search request.

# This function handle individual client search request.
# """
# def search_line_by_line(
#     file_path: str,
#     search_string: str,
#     reread_on_query: bool,
#     cached_lines: Optional[List[str]] = None,
# ) -> Union[bool, None]:
#     """
#     Search for an exact match of a string in a file or cached content.

#     If `reread_on_query` is True, the function reads the file directly 
#     on every query. Otherwise, it searches within the provided cached 
#     lines.

#     Args:
#         file_path (str): Path to the file to search.
#         search_string (str): The string to search for.
#         reread_on_query (bool): Whether to reread the file on each query.
#         cached_lines (Optional[List[str]]): Cached lines of the file.

#     Returns:
#         bool: True if the string is found, False otherwise.
#         None: If an error occurs (e.g., file not found).
#     """
#     try:
#         if reread_on_query:
#             # Read and search the file directly
#             with open(file_path, "r") as file:
#                 return any(line.strip() == search_string for line in file)
#         elif cached_lines is not None:
#             # Search within the cached lines
#             return any(line.strip() == search_string for line in cached_lines)
#         else:
#             logging.warning("No cached lines provided for search.")
#             return False
#     except FileNotFoundError:
#         logging.error(f"File not found: {file_path}")
#         return None
#     except Exception as error:
#         logging.error(f"Error reading file {file_path}: {error}")
#         return None


# def handle_reread_and_cache(
#     file_path: str, reread_on_query: bool, cached_lines: Optional[List[str]]
# ) -> Optional[List[str]]:
#     """
#     Handles logic for rereading the file or using cached lines.
#     """
#     if reread_on_query:
#         try:
#             with open(file_path, "r") as file:
#                 return file.readlines()
#         except FileNotFoundError:
#             logging.error(f"File not found: {file_path}")
#             return None
#         except Exception as e:
#             logging.error(f"Error reading file {file_path}: {e}")
#             return None
#     elif cached_lines is not None:
#         return cached_lines
#     else:
#         logging.warning("No cached lines provided for search.")
#         return None


# # Algorithm 2: Regex Search
# def regex_search(
#     file_path: str,
#     search_string: str,
#     reread_on_query: bool,
#     cached_lines: Optional[List[str]] = None,
# ) -> Union[bool, None]:
#     """
#     Search for a string in a file using a regex pattern.
#     """
#     lines = handle_reread_and_cache(file_path, reread_on_query, cached_lines)
#     if lines is None:
#         return None
#     pattern = re.compile(re.escape(search_string))
#     return any(pattern.search(line) for line in lines)


# # Algorithm 3: Binary Search on Sorted Lines
# def binary_search_sorted(
#     file_path: str,
#     search_string: str,
#     reread_on_query: bool,
#     cached_lines: Optional[List[str]] = None,
# ) -> Union[bool, None]:
#     """
#     Perform binary search on sorted lines of a file or cached content.
#     """
#     lines = handle_reread_and_cache(file_path, reread_on_query, cached_lines)
#     if lines is None:
#         return None
#     sorted_lines = sorted(line.strip() for line in lines)
#     idx = bisect_left(sorted_lines, search_string)
#     return idx < len(sorted_lines) and sorted_lines[idx] == search_string


# # Algorithm 4: In-Memory Set Lookup
# def in_memory_set_lookup(
#     file_path: str,
#     search_string: str,
#     reread_on_query: bool,
#     cached_lines: Optional[List[str]] = None,
# ) -> Union[bool, None]:
#     """
#     Use in-memory set for fast lookup.
#     """
#     lines = handle_reread_and_cache(file_path, reread_on_query, cached_lines)
#     if lines is None:
#         return None
#     lines_set = set(line.strip() for line in lines)
#     return search_string in lines_set


# # Algorithm 5: Linux `grep` Command Integration
# def linux_grep_search(
#     file_path: str,
#     search_string: str,
#     reread_on_query: bool,
#     cached_lines: Optional[List[str]] = None,
# ) -> Union[bool, None]:
#     """
#     Use the Linux `grep` command for searching.
#     """
#     if reread_on_query:
#         try:
#             result = subprocess.run(
#                 ["grep", "-Fxq", search_string, file_path], capture_output=True
#             )
#             return result.returncode == 0
#         except Exception as e:
#             logging.error(f"Error in linux_grep_search: {e}")
#             return None
#     else:
#         lines = handle_reread_and_cache(file_path, reread_on_query, cached_lines)
#         if lines is None:
#             return None
#         return any(line.strip() == search_string for line in lines)


# # Algorithm 6: Multithreaded Search
# def multithreaded_search(
#     file_path: str,
#     search_string: str,
#     reread_on_query: bool,
#     cached_lines: Optional[List[str]] = None,
# ) -> Union[bool, None]:
#     """
#     Perform multithreaded search on file content.
#     """
#     def search_chunk(lines: List[str]) -> bool:
#         return any(line.strip() == search_string for line in lines)

#     lines = handle_reread_and_cache(file_path, reread_on_query, cached_lines)
#     if lines is None:
#         return None

#     num_threads = 4  # Default number of threads
#     chunk_size = len(lines) // num_threads
#     chunks = [lines[i:i + chunk_size] for i in range(0, len(lines), chunk_size)]

#     with ThreadPoolExecutor(max_workers=num_threads) as executor:
#         results = executor.map(search_chunk, chunks)
#         return any(results)


# # Algorithm 7: Memory-Mapped Search
# def memory_mapped_search(
#     file_path: str,
#     search_string: str,
#     reread_on_query: bool,
#     cached_lines: Optional[List[str]] = None,
# ) -> Union[bool, None]:
#     """
#     Use memory mapping for searching in the file.
#     """
#     if reread_on_query:
#         try:
#             with open(file_path, "r+b") as file:
#                 with mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as mm:
#                     return search_string.encode("utf-8") in mm
#         except Exception as e:
#             logging.error(f"Error in memory_mapped_search: {e}")
#             return None
#     else:
#         lines = handle_reread_and_cache(file_path, reread_on_query, cached_lines)
#         if lines is None:
#             return None
#         return any(line.strip() == search_string for line in lines)

"""
Function to manage cache.

This function is called only once if reread on query is off.
"""
def load_file_into_cache(file_path: str) -> List[str]:
    """
    Load the file into memory and return its contents as a list of stripped lines.

    Args:
        file_path (str): Path to the file to load.

    Returns:
        List[str]: List of stripped lines from the file.
                   Returns an empty list if the file is not found or an error occurs.
    """
    try:
        with open(file_path, "r") as file:
            return [line.strip() for line in file]
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return []
    except Exception as error:
        logging.error(f"Error reading file {file_path}: {error}")
        return []

import logging
import subprocess
from typing import List, Optional, Union


"""
Function to manage client search request using Linux `grep`.

This function handles individual client search requests,
leveraging the Linux `grep` command or a cached
line-based search mechanism.
"""


def linux_grep_search(
    file_path: str,
    search_string: str,
    reread_on_query: bool,
    cached_lines: Optional[List[str]] = None,
) -> Union[bool, None]:
    """
    Search for an exact match of a string in a file
    using Linux `grep` or cached content.

    If `reread_on_query` is True, the function uses
    the Linux `grep` command to directly search the file.
    Otherwise, it searches within the provided cached lines.

    Args:
        file_path (str): Path to the file to search.
        search_string (str): The string to search for.
        reread_on_query (bool): Whether to reread the
        file using `grep` on each query.
        cached_lines (Optional[List[str]]): Cached lines of the file.

    Returns:
        bool: True if the string is found, False otherwise.
        None: If an error occurs
        (e.g., file not found or command failure).
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


"""
Function to manage cache.

This function is called only once if reread on query is off.
"""


def load_file_into_cache(file_path: str) -> List[str]:
    """
    Load the file into memory and return its contents
    as a list of stripped lines.

    Args:
        file_path (str): Path to the file to load.

    Returns:
        List[str]: List of stripped lines from the file.
                   Returns an empty list if the file is
                   not found or an error occurs.
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

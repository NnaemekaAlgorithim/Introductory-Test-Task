import logging
import mmap
from typing import Optional, Set, Union


"""
Module to manage client search request using mmap.
And Load the file into memory and return its content

The mmap search function efficiently handles client search
requests by using memory-mapped files to perform fast,
in-memory searches without loading the entire file into memory.
"""


def file_search(
    file_path: str,
    search_string: str,
    reread_on_query: bool,
    cached_lines: Optional[Set[str]] = None,
) -> Union[bool, None]:
    """
    Search for an exact match of a string in a file.

    Args:
        file_path (str): Path to the file to search.
        search_string (str): The string to search for.
        reread_on_query (bool): Whether to reread the file for each query.
        cached_lines (Optional[Set[str]]): Cached lines of the file.

    Returns:
        bool: True if the string is found, False otherwise.
        None: If an error occurs.
    """
    # Validate inputs
    if not file_path:
        logging.error("The file_path is empty or None.")
        return None
    if not search_string:
        logging.warning("The search_string is empty or None.")
        return False

    try:
        if reread_on_query:
            # Use mmap for efficient file searching
            with open(file_path, "rb") as f:
                with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                    # Search for the exact match of the search string
                    search_bytes = search_string.encode("utf-8")
                    offset = 0
                    while True:
                        found = mm.find(search_bytes, offset)
                        if found == -1:
                            break
                        # Check if the found match is a complete word
                        if (found == 0 or mm[found - 1] in b" \t\r\n"):
                            if (
                                    found + len(search_bytes) == len(mm) or
                                    mm[found + len(search_bytes)] in b" \t\r\n"
                            ):
                                return True
                            offset = found + 1

            return False  # No exact match found

        elif cached_lines is not None:
            # Use set for O(1) average lookup time
            return search_string in cached_lines
        else:
            logging.warning("No cached lines provided for search.")
            return False

    except FileNotFoundError:
        logging.error(
            f"File not found: {file_path}. Ensure the file exists."
        )
        return None
    except PermissionError:
        logging.error(
            f"Permission denied while accessing the file: {file_path}."
        )
        return None
    except OSError as os_error:
        logging.error(
            f"OS error occurred with file {file_path}: {os_error}"
        )
        return None
    except ValueError as value_error:
        logging.error(
            f"Value error while processing {file_path}: {value_error}"
        )
        return None
    except Exception as error:
        logging.error(
            f"Unexpected error in file_search: {error}"
        )
        return None


def load_file_into_cache(file_path: str) -> set:
    """
    Load the file into memory and return its contents
    as a set of stripped lines for fast searching.

    Args:
        file_path (str): Path to the file to load.

    Returns:
        set: Set of stripped lines from the file.
             Returns an empty set if the file is
             not found or an error occurs.
    """
    # Validate input
    if not file_path:
        logging.error("The file_path is empty or None.")
        return set()

    try:
        with open(file_path, "r") as file:
            return {line.strip() for line in file}
    except FileNotFoundError:
        logging.error(
            f"File not found: {file_path}. Ensure the file exists."
        )
        return set()
    except PermissionError:
        logging.error(
            f"Permission denied while accessing the file: {file_path}."
        )
        return set()
    except OSError as os_error:
        logging.error(
            f"OS error occurred with file {file_path}: {os_error}"
        )
        return set()
    except ValueError as value_error:
        logging.error(
            f"Value error while processing {file_path}: {value_error}"
        )
        return set()
    except Exception as error:
        logging.error(
            f"Unexpected error reading file {file_path}: {error}"
        )
        return set()

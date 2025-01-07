import logging

def search_in_file(file_path, search_string, reread_on_query, cached_lines=None):
    """Search for a full match of the string in the specified file or cached content."""
    try:
        if reread_on_query == "true":
            with open(file_path, 'r') as f:
                for line in f:
                    if line.strip() == search_string:
                        return True
            return False
        else:
            if cached_lines:
                for line in cached_lines:
                    if line.strip() == search_string:
                        return True
            return False
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return None
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {e}")
        return None

def load_file_into_cache(file_path):
    """Load the file into memory and return the contents."""
    try:
        with open(file_path, 'r') as f:
            return [line.strip() for line in f]
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return []
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {e}")
        return []

import os
import tempfile
import pytest
from unittest.mock import patch, mock_open
from py_server.file_utils import file_search, load_file_into_cache


@pytest.fixture
def temp_file():
    """Fixture to create a temporary file for testing."""
    with tempfile.NamedTemporaryFile(delete=False, mode="w+t") as temp:
        temp.write("line1\nline2\nsearch_this_line\n")
        temp.flush()
        yield temp.name
    os.unlink(temp.name)


def test_file_search_with_mmap(temp_file):
    """Test file_search with mmap and a valid search string."""
    assert file_search(
        temp_file, "search_this_line", reread_on_query=True
    ) is True
    assert file_search(
        temp_file, "non_existent_line", reread_on_query=True
    ) is False


def test_file_search_with_cached_lines():
    """Test file_search using cached lines."""
    cached_lines = {"line1", "line2", "search_this_line"}
    assert file_search(
        "dummy_path",
        "search_this_line",
        reread_on_query=False,
        cached_lines=cached_lines
    ) is True
    assert file_search(
        "dummy_path",
        "non_existent_line",
        reread_on_query=False,
        cached_lines=cached_lines
    ) is False


def test_file_search_with_no_cached_lines():
    """Test file_search when no cached lines are provided."""
    assert file_search(
        "dummy_path",
        "search_this_line",
        reread_on_query=False
    ) is False


def test_file_search_file_not_found():
    """Test file_search when the file does not exist."""
    with patch(
            "builtins.open",
            side_effect=FileNotFoundError):
        assert file_search(
            "non_existent_file",
            "search_string",
            reread_on_query=True
        ) is None


def test_file_search_permission_error():
    """Test file_search when file access is denied."""
    with patch(
            "builtins.open",
            side_effect=PermissionError):
        assert file_search(
            "restricted_file",
            "search_string",
            reread_on_query=True
        ) is None


def test_file_search_os_error():
    """Test file_search when an OS error occurs."""
    with patch(
            "builtins.open",
            side_effect=OSError("OS error")):
        assert file_search(
            "error_file",
            "search_string",
            reread_on_query=True
        ) is None


def test_file_search_value_error():
    """Test file_search when a ValueError occurs."""
    with patch(
            "mmap.mmap",
            side_effect=ValueError("Value error")):
        with open(
            tempfile.NamedTemporaryFile(delete=False).name, "wb"
        ) as dummy_file:
            dummy_file.write(b"dummy_content")
        assert file_search(
            dummy_file.name,
            "search_string",
            reread_on_query=True
        ) is None


def test_load_file_into_cache(temp_file):
    """Test load_file_into_cache for successful loading."""
    cached_lines = load_file_into_cache(temp_file)
    assert cached_lines == {"line1", "line2", "search_this_line"}


def test_load_file_into_cache_file_not_found():
    """Test load_file_into_cache when the file does not exist."""
    with patch("builtins.open", side_effect=FileNotFoundError):
        assert load_file_into_cache("non_existent_file") == set()


def test_load_file_into_cache_permission_error():
    """Test load_file_into_cache when file access is denied."""
    with patch("builtins.open", side_effect=PermissionError):
        assert load_file_into_cache("restricted_file") == set()


def test_load_file_into_cache_os_error():
    """Test load_file_into_cache when an OS error occurs."""
    with patch("builtins.open", side_effect=OSError("OS error")):
        assert load_file_into_cache("error_file") == set()


def test_load_file_into_cache_value_error():
    """Test load_file_into_cache when a ValueError occurs."""
    with patch(
        "builtins.open", mock_open(read_data="line1\nline2\nsearch_this_line")
            ), \
         patch("builtins.open", side_effect=ValueError("Value error")):
        assert load_file_into_cache("dummy_path") == set()

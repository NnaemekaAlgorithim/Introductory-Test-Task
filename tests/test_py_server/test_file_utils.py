import pytest
from unittest.mock import patch
from py_server.file_utils import linux_grep_search, load_file_into_cache


# Function to test linux_grep_search
@pytest.mark.parametrize(
    "file_path, search_string, reread_on_query, cached_lines, expected_result",
    [
        ("test.txt", "search_term", True, None, True),
        ("test.txt", "search_term", False, ["line1", "search_term"], True),
        ("test.txt", "search_term", False, None, False),
        ("nonexistent.txt", "search_term", True, None, False),
        ("test.txt", "search_term", True, None, True),
    ]
)
@patch("subprocess.run")
def test_linux_grep_search(
    mock_run,
    file_path,
    search_string,
    reread_on_query,
    cached_lines,
    expected_result
):
    """
    Test the `linux_grep_search` function for various scenarios.
    """
    # Mock subprocess.run to simulate command behavior
    if reread_on_query and file_path != "nonexistent.txt":
        mock_run.return_value.returncode = 0  # Simulating grep success
    else:
        mock_run.return_value.returncode = 1  # Simulating grep failure

    result = linux_grep_search(
        file_path,
        search_string,
        reread_on_query,
        cached_lines
    )

    assert result == expected_result


@pytest.mark.parametrize(
    "file_path, expected_result",
    [
        ("test.txt", []),  # File with valid content
        ("nonexistent.txt", []),  # File does not exist
        ("empty.txt", []),  # Empty file
    ]
)
@patch("builtins.open")
def test_load_file_into_cache(mock_open, file_path, expected_result):
    """
    Test the `load_file_into_cache` function for various scenarios.
    """
    # Mocking open function behavior
    if file_path == "test.txt":
        # Mock the file contents for a valid file
        mock_file = mock_open.return_value
        mock_enter = mock_file.__enter__.return_value
        mock_enter.readlines.return_value = ["line1\n", "line2\n"]
    elif file_path == "empty.txt":
        # Mock an empty file
        mock_file = mock_open.return_value
        mock_enter = mock_file.__enter__.return_value
        mock_enter.readlines.return_value = []
    else:
        # Simulate file not found error
        mock_open.side_effect = FileNotFoundError

    result = load_file_into_cache(file_path)

    # Assert that the result matches the expected result
    assert result == expected_result


# Edge case: handle invalid arguments and logging errors

@pytest.mark.parametrize(
    "file_path, search_string, reread_on_query, cached_lines, expected_result",
    [
        (None, "search_term", True, None, None),
        ("test.txt", None, True, None, None),
        ("test.txt", "search_term", None, False, None),
    ]
)
def test_linux_grep_search_edge_cases(
    file_path,
    search_string,
    reread_on_query,
    cached_lines,
    expected_result
):
    """
    Test edge cases for `linux_grep_search`
    when provided with invalid arguments.
    """
    result = linux_grep_search(
        file_path,
        search_string,
        reread_on_query,
        cached_lines
    )

    assert result == expected_result

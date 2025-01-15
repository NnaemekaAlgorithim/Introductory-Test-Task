# import pytest
# from unittest import mock
# import os
# import time

# from py_server.file_utils import load_file_into_cache, search_in_file

# @pytest.fixture
# def mock_file_content():
#     """Mock content of the file."""
#     return "This is a sample line in the file.\nAnother line."

# @pytest.fixture
# def mock_file_path(mock_file_content):
#     """Create a mock file for testing."""
#     file_path = "test_file.txt"
#     with open(file_path, "w") as file:
#         file.write(mock_file_content)
#     yield file_path
#     os.remove(file_path)  # Clean up after test

# def test_search_in_file_found(mock_file_path):
#     """Test for valid search where the string is found in the file."""
#     result = search_in_file(mock_file_path, "This is a sample line in the file.", False)
#     assert result is True

# def test_search_in_file_not_found(mock_file_path):
#     """Test for valid search where the string is not found in the file."""
#     result = search_in_file(mock_file_path, "Non-existing string", False)
#     assert result is False

# def test_search_in_file_with_cache():
#     """Test for valid search when cached lines are used."""
#     cached_lines = ["Line 1", "Line 2", "Search this line"]
#     result = search_in_file("dummy_path.txt", "Search this line", False, cached_lines)
#     assert result is True

# def test_search_in_file_file_not_found():
#     """Test for search when the file is not found."""
#     with mock.patch("builtins.open", mock.MagicMock(side_effect=FileNotFoundError)):
#         result = search_in_file("non_existent_file.txt", "Any search string", True)
#         assert result is None

# def test_search_in_file_general_error():
#     """Test for general error when accessing file."""
#     with mock.patch("builtins.open", mock.MagicMock(side_effect=PermissionError)):
#         result = search_in_file("test_file.txt", "Any search string", True)
#         assert result is None

# def test_load_file_into_cache(mock_file_path):
#     """Test loading the file into memory as a cache."""
#     result = load_file_into_cache(mock_file_path)
#     assert result == ["This is a sample line in the file.", "Another line."]

# def test_load_file_into_cache_file_not_found():
#     """Test for file not found error while loading into cache."""
#     result = load_file_into_cache("non_existent_file.txt")
#     assert result == []

# def test_load_file_into_cache_general_error():
#     """Test for general error when loading file into cache."""
#     with mock.patch("builtins.open", mock.MagicMock(side_effect=PermissionError)):
#         result = load_file_into_cache("test_file.txt")
#         assert result == []

# def test_load_file_into_cache_empty_file():
#     """Test for loading an empty file into cache."""
#     empty_file_path = "empty_file.txt"
#     with open(empty_file_path, "w") as f:
#         f.write("")
    
#     result = load_file_into_cache(empty_file_path)
#     assert result == []
    
#     os.remove(empty_file_path)  # Clean up

# def test_search_in_large_file():
#     """Test performance of searching in large file."""
#     large_file_path = "large_file.txt"
#     with open(large_file_path, "w") as f:
#         f.write("A" * 10**6)  # Create a large file with 1 million characters

#     start_time = time.time()
#     result = search_in_file(large_file_path, "A" * 100, False)
#     elapsed_time = time.time() - start_time
#     print(f"Time to search in large file: {elapsed_time:.2f} seconds")
#     assert elapsed_time < 2  # Example threshold for performance

#     os.remove(large_file_path)  # Clean up

# def test_search_in_file_file_not_found(caplog):
#     """Test file not found error and capture log."""
#     with mock.patch("builtins.open", mock.MagicMock(side_effect=FileNotFoundError)):
#         result = search_in_file("non_existent_file.txt", "Any search string", True)
#         assert result is None
#         assert "File not found" in caplog.text

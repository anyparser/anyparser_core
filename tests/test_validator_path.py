import os
import sys
from pathlib import Path

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from anyparser_core.validator.path import validate_path
from anyparser_core.validator.validation import (
    InvalidPathValidationResult,
    ValidPathValidationResult,
)


@pytest.fixture
def sample_file(tmp_path):
    file_path = tmp_path / "test.txt"
    file_path.write_text("Hello, World!")
    return str(file_path)


@pytest.mark.asyncio
async def test_validate_path_single_string():
    """Test validation with single file path as string"""
    with open("temp.txt", "w") as f:
        f.write("test")

    try:
        result = await validate_path("temp.txt")
        assert isinstance(result, ValidPathValidationResult)
        assert result.files == ["temp.txt"]
        assert result.valid is True
    finally:
        os.remove("temp.txt")


@pytest.mark.asyncio
async def test_validate_path_single_path():
    """Test validation with single file path as Path object"""
    path = Path("temp.txt")
    path.write_text("test")

    try:
        result = await validate_path(path)
        assert isinstance(result, ValidPathValidationResult)
        assert result.files == [path]
        assert result.valid is True
    finally:
        path.unlink()


@pytest.mark.asyncio
async def test_validate_path_multiple_files(tmp_path):
    """Test validation with multiple file paths"""
    file1 = tmp_path / "test1.txt"
    file2 = tmp_path / "test2.txt"
    file1.write_text("File 1")
    file2.write_text("File 2")

    result = await validate_path([str(file1), str(file2)])
    assert isinstance(result, ValidPathValidationResult)
    assert len(result.files) == 2
    assert str(file1) in result.files
    assert str(file2) in result.files
    assert result.valid is True


@pytest.mark.asyncio
async def test_validate_path_nonexistent_file():
    """Test validation with nonexistent file"""
    result = await validate_path("nonexistent.txt")
    assert isinstance(result, InvalidPathValidationResult)
    assert isinstance(result.error, FileNotFoundError)
    assert "File does not exist: nonexistent.txt" in str(result.error)
    assert result.valid is False


@pytest.mark.asyncio
async def test_validate_path_mixed_files(tmp_path):
    """Test validation with mix of existing and nonexistent files"""
    file1 = tmp_path / "test1.txt"
    file1.write_text("File 1")

    result = await validate_path([str(file1), "nonexistent.txt"])
    assert isinstance(result, InvalidPathValidationResult)
    assert isinstance(result.error, FileNotFoundError)
    assert "File does not exist: nonexistent.txt" in str(result.error)
    assert result.valid is False


@pytest.mark.asyncio
async def test_validate_path_empty():
    """Test validation with empty or whitespace file paths"""
    # Test empty string
    result = await validate_path("")
    assert isinstance(result, InvalidPathValidationResult)
    assert isinstance(result.error, FileNotFoundError)
    assert "No files provided" in str(result.error)
    assert result.valid is False

    # Test whitespace string
    result = await validate_path("   ")
    assert isinstance(result, InvalidPathValidationResult)
    assert isinstance(result.error, FileNotFoundError)
    assert "No files provided" in str(result.error)
    assert result.valid is False

    # Test empty list
    result = await validate_path([])
    assert isinstance(result, InvalidPathValidationResult)
    assert isinstance(result.error, FileNotFoundError)
    assert "No files provided" in str(result.error)
    assert result.valid is False

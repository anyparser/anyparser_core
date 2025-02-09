import os
import sys
from pathlib import Path
from typing import List

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from anyparser_core.config.hardcoded import OcrLanguage, OCRPreset
from anyparser_core.options import AnyparserOption, AnyparserParsedOption
from anyparser_core.validator.main import validate_and_parse
from anyparser_core.validator.url import InvalidUrlError


@pytest.fixture
def mock_api_key():
    return "test-api-key-12345"


@pytest.fixture
def sample_file(tmp_path):
    file_path = tmp_path / "test.txt"
    file_path.write_text("Hello, World!")
    return str(file_path)


@pytest.mark.asyncio
async def test_validate_and_parse_single_file(tmp_path, monkeypatch, mock_api_key):
    monkeypatch.setenv("ANYPARSER_API_KEY", mock_api_key)
    """Test validation and parsing of a single file."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("test content")

    result = await validate_and_parse(str(test_file))
    assert result.files is not None
    assert len(result.files) == 1
    assert result.files[0].filename == "test.txt"


@pytest.mark.asyncio
async def test_validate_and_parse_multiple_files(tmp_path, monkeypatch, mock_api_key):
    monkeypatch.setenv("ANYPARSER_API_KEY", mock_api_key)
    """Test validation and parsing of multiple files."""
    files: List[Path] = []
    for i in range(3):
        file = tmp_path / f"test{i}.txt"
        file.write_text(f"test content {i}")
        files.append(file)

    result = await validate_and_parse([str(f) for f in files])
    assert result.files is not None
    assert len(result.files) == 3
    assert all(f.filename.startswith("test") for f in result.files)


@pytest.mark.asyncio
async def test_validate_and_parse_crawler(monkeypatch, mock_api_key):
    monkeypatch.setenv("ANYPARSER_API_KEY", mock_api_key)
    """Test validation and parsing for crawler mode."""
    options = AnyparserOption(
        model="crawler",
        api_url="https://api.example.com",
        api_key="test-key",
    )
    result = await validate_and_parse("https://anyparser.com", options)
    assert result.url == "https://anyparser.com"
    assert result.files is None


@pytest.mark.asyncio
async def test_validate_and_parse_invalid_url(monkeypatch, mock_api_key):
    monkeypatch.setenv("ANYPARSER_API_KEY", mock_api_key)
    """Test validation and parsing with invalid URL in crawler mode."""
    options = AnyparserOption(
        model="crawler",
        api_url="https://api.example.com",
        api_key="test-key",
    )
    with pytest.raises(InvalidUrlError):
        await validate_and_parse("not-a-url", options)


@pytest.mark.asyncio
async def test_validate_and_parse_empty_files_crawler(monkeypatch, mock_api_key):
    monkeypatch.setenv("ANYPARSER_API_KEY", mock_api_key)
    """Test validation and parsing in crawler mode with empty files list."""
    options = AnyparserOption(
        model="crawler",
        api_url="https://api.example.com",
        api_key="test-key",
    )

    # Mock validate_url to return invalid URL result
    from anyparser_core.validator.url import InvalidUrlError
    from anyparser_core.validator.validation import InvalidPathValidationResult

    async def mock_validate_url(url):
        return InvalidPathValidationResult(
            error=InvalidUrlError(url=url, reason="Invalid URL")
        )

    import anyparser_core.validator.main

    original_validate_url = anyparser_core.validator.main.validate_url
    anyparser_core.validator.main.validate_url = mock_validate_url

    try:
        with pytest.raises(InvalidUrlError):
            await validate_and_parse("https://example.com", options)
    finally:
        # Restore original function
        anyparser_core.validator.main.validate_url = original_validate_url


@pytest.mark.asyncio
async def test_validate_and_parse_missing_file(monkeypatch, mock_api_key):
    monkeypatch.setenv("ANYPARSER_API_KEY", mock_api_key)
    """Test validation and parsing with non-existent file."""
    with pytest.raises(FileNotFoundError):
        await validate_and_parse("nonexistent.txt")


@pytest.mark.asyncio
async def test_validate_and_parse_with_options(tmp_path, monkeypatch, mock_api_key):
    monkeypatch.setenv("ANYPARSER_API_KEY", mock_api_key)
    """Test validation and parsing with custom options."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("test content")

    options = AnyparserOption(
        format="markdown",
        model="text",
        image=True,
        table=True,
        api_url="https://api.example.com",
        api_key="test-key",
    )

    result = await validate_and_parse(str(test_file), options)
    assert result.format == "markdown"
    assert result.model == "text"
    assert result.image is True
    assert result.table is True


@pytest.mark.asyncio
async def test_validate_and_parse_with_ocr_options(
    sample_file, monkeypatch, mock_api_key
):
    monkeypatch.setenv("ANYPARSER_API_KEY", mock_api_key)
    """Test validating and parsing with OCR options"""
    options = AnyparserOption(
        api_url="https://api.example.com",
        api_key="test-key",
        ocr_language=[OcrLanguage.ENGLISH, OcrLanguage.SPANISH],
        ocr_preset=OCRPreset.DOCUMENT,
    )

    result = await validate_and_parse(sample_file, options)

    assert result.ocr_language == [OcrLanguage.ENGLISH, OcrLanguage.SPANISH]
    assert result.ocr_preset == OCRPreset.DOCUMENT


@pytest.mark.asyncio
async def test_validate_and_parse_invalid_file(monkeypatch, mock_api_key):
    monkeypatch.setenv("ANYPARSER_API_KEY", mock_api_key)
    """Test validating and parsing with invalid file"""
    options = AnyparserOption(api_url="https://api.example.com", api_key="test-key")

    with pytest.raises(FileNotFoundError):
        await validate_and_parse("nonexistent.txt", options)


@pytest.mark.asyncio
async def test_validate_and_parse_default_options(
    sample_file, monkeypatch, mock_api_key
):
    monkeypatch.setenv("ANYPARSER_API_KEY", mock_api_key)
    """Test validating and parsing with default options"""
    result = await validate_and_parse(sample_file)
    assert result.format == "json"
    assert result.model == "text"
    assert result.image is True


@pytest.mark.asyncio
async def test_validate_and_parse_with_path_object(
    sample_file, monkeypatch, mock_api_key
):
    monkeypatch.setenv("ANYPARSER_API_KEY", mock_api_key)
    """Test validating and parsing with Path object"""
    from pathlib import Path

    result = await validate_and_parse(Path(sample_file))
    assert isinstance(result, AnyparserParsedOption)
    assert len(result.files) == 1


@pytest.mark.asyncio
async def test_validate_and_parse_file_removed(tmp_path, monkeypatch, mock_api_key):
    monkeypatch.setenv("ANYPARSER_API_KEY", mock_api_key)
    """Test validating and parsing when file is removed during processing"""
    test_file = tmp_path / "test.txt"
    test_file.write_text("test content")

    # Mock file reading to simulate file being removed during processing
    def mock_read(*args, **kwargs):
        raise FileNotFoundError(f"File {test_file} was not found or was removed")

    monkeypatch.setattr("builtins.open", mock_read)

    with pytest.raises(FileNotFoundError, match="was not found or was removed"):
        await validate_and_parse(str(test_file))


@pytest.mark.asyncio
async def test_validate_and_parse_file_not_found(monkeypatch, mock_api_key):
    monkeypatch.setenv("ANYPARSER_API_KEY", mock_api_key)
    """Test validating and parsing when file does not exist"""
    with pytest.raises(FileNotFoundError, match="File does not exist"):
        await validate_and_parse("/path/to/nonexistent/file.txt")


@pytest.mark.asyncio
async def test_validate_and_parse_file_locked(tmp_path, monkeypatch, mock_api_key):
    monkeypatch.setenv("ANYPARSER_API_KEY", mock_api_key)
    """Test validating and parsing when file is locked by another process"""
    test_file = tmp_path / "test.txt"
    test_file.write_text("test content")

    # Mock file locking to simulate BlockingIOError
    def mock_flock(*args, **kwargs):
        raise BlockingIOError("File is locked")

    monkeypatch.setattr("fcntl.flock", mock_flock)

    with pytest.raises(IOError, match="is locked by another process"):
        await validate_and_parse(str(test_file))

from unittest.mock import patch

import pytest

from anyparser_core.validator.url import InvalidUrlError, validate_url


@pytest.mark.asyncio
async def test_validate_url_valid():
    """Test validation of a valid URL."""
    result = await validate_url("https://anyparser.com")
    assert result.valid
    assert result.files == ["https://anyparser.com"]


@pytest.mark.asyncio
async def test_validate_url_invalid():
    """Test validation of an invalid URL."""
    result = await validate_url("not-a-url")
    assert not result.valid
    assert isinstance(result.error, InvalidUrlError)
    assert result.error.url == "not-a-url"
    assert str(result.error) == "The URL 'not-a-url' is invalid."


@pytest.mark.asyncio
async def test_validate_url_empty():
    """Test validation of an empty URL."""
    result = await validate_url("")
    assert not result.valid
    assert isinstance(result.error, InvalidUrlError)


@pytest.mark.asyncio
async def test_validate_url_special_chars():
    """Test validation of URLs with special characters."""
    result = await validate_url("https://example.com/path with spaces")
    assert result.valid
    assert result.files == ["https://example.com/path with spaces"]


@pytest.mark.asyncio
async def test_validate_url_missing_scheme():
    """Test validation of URL without scheme."""
    result = await validate_url("example.com")
    assert not result.valid
    assert isinstance(result.error, InvalidUrlError)


@pytest.mark.asyncio
async def test_validate_url_parse_error():
    """Test validation when URL parsing raises an exception."""
    with patch("anyparser_core.validator.url.urlparse") as mock_urlparse:
        mock_urlparse.side_effect = ValueError("Forced exception")
        result = await validate_url("https://example.com")
        assert not result.valid
        assert isinstance(result.error, InvalidUrlError)


@pytest.mark.asyncio
async def test_validate_url_missing_netloc():
    """Test validation of URL without netloc."""
    result = await validate_url("https:///path")
    assert not result.valid
    assert isinstance(result.error, InvalidUrlError)


@pytest.mark.asyncio
async def test_validate_url_unsupported_scheme():
    """Test validation of URL with unsupported scheme."""
    result = await validate_url("ftp://example.com")
    assert not result.valid
    assert isinstance(result.error, InvalidUrlError)
    assert "Invalid scheme 'ftp'" in str(result.error.reason)


@pytest.mark.asyncio
async def test_validate_url_with_reason():
    """Test URL validation error with reason."""
    error = InvalidUrlError("test.com", reason="Custom error reason")
    assert error.url == "test.com"
    assert error.reason == "Custom error reason"

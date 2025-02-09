import os
import sys

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import http.client
import json
from unittest.mock import Mock, patch

from anyparser_core import (
    Anyparser,
    AnyparserCrawlResult,
    AnyparserPdfPage,
    AnyparserPdfResult,
)
from anyparser_core.options import AnyparserOption, AnyparserParsedOption, UploadedFile


@pytest.fixture
def mock_response():
    response = Mock()
    response.status = 200
    return response


@pytest.fixture
def sample_json_response():
    return json.dumps(
        [
            {
                "rid": "test123",
                "original_filename": "test.pdf",
                "checksum": "abc123",
                "markdown": "# Test",
                "total_characters": 100,
                "total_items": 1,
                "items": [
                    {
                        "page_number": 1,
                        "markdown": "# Page 1",
                        "text": "Page 1 content",
                        "images": ["image1.png"],
                    }
                ],
            }
        ]
    ).encode()


@pytest.mark.asyncio
async def test_parse_single_file(mock_response, sample_json_response):
    """Test parsing a single file with JSON response"""
    mock_response.read.return_value = sample_json_response

    with (
        patch("anyparser_core.parser.async_request", return_value=mock_response),
        patch("anyparser_core.parser.validate_and_parse") as mock_validate,
    ):

        # Setup mock validate_and_parse
        mock_validate.return_value = AnyparserParsedOption(
            files=[UploadedFile(filename="test.pdf", contents=b"test")],
            api_url="https://api.example.com",
            api_key="test-key",
            format="json",
        )

        parser = Anyparser(
            AnyparserOption(api_url="https://api.example.com", api_key="test-key")
        )

        result = await parser.parse("test.pdf")

        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], (AnyparserPdfResult, AnyparserCrawlResult))
        assert result[0].rid == "test123"
        assert result[0].original_filename == "test.pdf"
        assert result[0].total_items == 1

        # Check PDF page parsing
        assert len(result[0].items) == 1
        page = result[0].items[0]
        assert isinstance(page, AnyparserPdfPage)
        assert page.page_number == 1
        assert page.markdown == "# Page 1"
        assert page.text == "Page 1 content"
        assert page.images == ["image1.png"]


@pytest.mark.asyncio
async def test_parse_text_format(mock_response):
    """Test parsing with text format response"""
    mock_response.read.return_value = b"Plain text response"

    with (
        patch("anyparser_core.parser.async_request", return_value=mock_response),
        patch("anyparser_core.parser.validate_and_parse") as mock_validate,
    ):

        # Setup mock validate_and_parse
        mock_validate.return_value = AnyparserParsedOption(
            files=[UploadedFile(filename="test.txt", contents=b"test")],
            api_url="https://api.example.com",
            api_key="test-key",
            format="markdown",
        )

        parser = Anyparser(
            AnyparserOption(
                api_url="https://api.example.com",
                api_key="test-key",
                format="markdown",  # Non-JSON format
            )
        )

        result = await parser.parse("test.txt")
        assert isinstance(result, str)
        assert result == "Plain text response"


@pytest.mark.asyncio
async def test_parse_error_response():
    """Test handling of error responses"""
    error_response = Mock()
    error_response.status = 400
    error_response.read.return_value = b"Bad Request"

    with (
        patch("anyparser_core.parser.async_request", return_value=error_response),
        patch("anyparser_core.parser.validate_and_parse") as mock_validate,
    ):

        # Setup mock validate_and_parse
        mock_validate.return_value = AnyparserParsedOption(
            files=[UploadedFile(filename="test.pdf", contents=b"test")],
            api_url="https://api.example.com",
            api_key="test-key",
            format="json",
        )

        parser = Anyparser(
            AnyparserOption(api_url="https://api.example.com", api_key="test-key")
        )

        with pytest.raises(http.client.HTTPException) as exc_info:
            await parser.parse("test.pdf")

        assert "HTTP 400" in str(exc_info.value)


@pytest.mark.asyncio
async def test_parse_multiple_files(mock_response):
    """Test parsing multiple files"""
    multiple_files_response = json.dumps(
        [
            {
                "rid": "test1",
                "original_filename": "test1.pdf",
                "checksum": "abc123",
                "markdown": "# Test 1",
                "total_characters": 100,
            },
            {
                "rid": "test2",
                "original_filename": "test2.pdf",
                "checksum": "def456",
                "markdown": "# Test 2",
                "total_characters": 200,
            },
        ]
    ).encode()

    mock_response.read.return_value = multiple_files_response

    with (
        patch("anyparser_core.parser.async_request", return_value=mock_response),
        patch("anyparser_core.parser.validate_and_parse") as mock_validate,
    ):

        # Setup mock validate_and_parse
        mock_validate.return_value = AnyparserParsedOption(
            files=[
                UploadedFile(filename="test1.pdf", contents=b"test1"),
                UploadedFile(filename="test2.pdf", contents=b"test2"),
            ],
            api_url="https://api.example.com",
            api_key="test-key",
            format="json",
        )

        parser = Anyparser(
            AnyparserOption(api_url="https://api.example.com", api_key="test-key")
        )

        result = await parser.parse(["test1.pdf", "test2.pdf"])

        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0].rid == "test1"
        assert result[1].rid == "test2"


@pytest.mark.asyncio
async def test_parse_crawler_mode(mock_response):
    """Test parsing in crawler mode"""
    crawler_response = json.dumps(
        [
            {
                "rid": "crawler1",
                "start_url": "https://example.com",
                "total_characters": 1000,
                "total_items": 2,
                "markdown": "# Crawl Results",
                "items": [
                    {
                        "url": "https://example.com",
                        "status_code": 200,
                        "status_message": "OK",
                        "politeness_delay": 1000,
                        "total_characters": 500,
                        "markdown": "# Page 1",
                        "directive": {
                            "type": "Combined",
                            "priority": 0,
                            "name": None,
                            "noindex": False,
                            "nofollow": False,
                            "underlying": [
                                {
                                    "type": "Meta",
                                    "priority": 1,
                                    "name": "robots",
                                    "noindex": False,
                                    "nofollow": False,
                                }
                            ],
                        },
                        "title": "Example Page",
                        "crawled_at": "2024-03-20T12:00:00Z",
                    }
                ],
                "robots_directive": {
                    "user_agent": "*",
                    "allow": ["/"],
                    "disallow": ["/private"],
                    "crawl_delay": 1,
                },
            }
        ]
    ).encode()

    mock_response.read.return_value = crawler_response

    with (
        patch("anyparser_core.parser.async_request", return_value=mock_response),
        patch("anyparser_core.parser.validate_and_parse") as mock_validate,
    ):
        # Setup mock validate_and_parse
        mock_validate.return_value = AnyparserParsedOption(
            url="https://example.com",
            api_url="https://api.example.com",
            api_key="test-key",
            format="json",
            model="crawler",
        )

        parser = Anyparser(
            AnyparserOption(
                api_url="https://api.example.com", api_key="test-key", model="crawler"
            )
        )

        result = await parser.parse("https://example.com")

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].rid == "crawler1"
        assert result[0].start_url == "https://example.com"
        assert result[0].total_items == 2
        assert len(result[0].items) == 1

        # Check crawler-specific fields
        item = result[0].items[0]
        assert item.url == "https://example.com"
        assert item.status_code == 200
        assert item.title == "Example Page"
        assert item.directive.type == "Combined"
        assert len(item.directive.underlying) == 1

        # Check robots.txt directive
        assert result[0].robots_directive.user_agent == "*"
        assert result[0].robots_directive.allow == ["/"]
        assert result[0].robots_directive.disallow == ["/private"]
        assert result[0].robots_directive.crawl_delay == 1

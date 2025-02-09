import os
import sys

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import http.client
from unittest.mock import Mock

from anyparser_core.request import async_request


@pytest.mark.asyncio
async def test_async_request():
    """Test async_request function with mocked connection"""
    # Mock connection and response
    mock_conn = Mock(spec=http.client.HTTPSConnection)
    mock_response = Mock(spec=http.client.HTTPResponse)
    mock_conn.getresponse.return_value = mock_response

    # Test parameters
    method = "POST"
    url = "/test"
    body = b"test data"
    headers = {"Content-Type": "application/json"}

    # Make the request
    response = await async_request(mock_conn, method, url, body, headers)

    # Verify the connection was used correctly
    mock_conn.request.assert_called_once_with(method, url, body, headers)
    mock_conn.getresponse.assert_called_once()

    # Verify we got the mock response back
    assert response == mock_response


@pytest.mark.asyncio
async def test_async_request_with_error():
    """Test async_request function with connection error"""
    mock_conn = Mock(spec=http.client.HTTPSConnection)
    mock_conn.request.side_effect = http.client.HTTPException("Connection failed")

    with pytest.raises(http.client.HTTPException) as exc_info:
        await async_request(
            mock_conn,
            "POST",
            "/test",
            b"test data",
            {"Content-Type": "application/json"},
        )

    assert "Connection failed" in str(exc_info.value)


@pytest.mark.asyncio
async def test_async_request_large_payload():
    """Test async_request with a large payload"""
    mock_conn = Mock(spec=http.client.HTTPSConnection)
    mock_response = Mock(spec=http.client.HTTPResponse)
    mock_conn.getresponse.return_value = mock_response

    # Create a large payload
    large_payload = b"x" * 1024 * 1024  # 1MB of data

    response = await async_request(
        mock_conn,
        "POST",
        "/test",
        large_payload,
        {"Content-Type": "application/octet-stream"},
    )

    mock_conn.request.assert_called_once()
    assert response == mock_response

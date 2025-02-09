import asyncio
import http.client
from http.client import HTTPResponse
from typing import Dict


async def async_request(
    conn: http.client.HTTPSConnection,
    method: str,
    url: str,
    body: bytes,
    headers: Dict[str, str],
) -> HTTPResponse:
    """
    Helper function to make an HTTP request asynchronously using asyncio.

    Args:
        conn: HTTP connection object
        method: HTTP method (GET, POST, etc.)
        url: Request URL
        body: Request body as bytes
        headers: Request headers

    Returns:
        HTTPResponse object containing the server's response
    """
    loop = asyncio.get_event_loop()

    # Asynchronously send the request and get the response (using thread pool for non-blocking)
    future = loop.run_in_executor(None, conn.request, method, url, body, headers)
    await future

    # Read the response asynchronously
    future = loop.run_in_executor(None, conn.getresponse)
    response = await future

    return response

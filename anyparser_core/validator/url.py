"""
Validation module for URLs
"""

from urllib.parse import urlparse

from anyparser_core.validator.validation import (
    InvalidPathValidationResult,
    PathValidationResult,
    ValidPathValidationResult,
)


class InvalidUrlError(Exception):
    """Custom exception for invalid URL."""

    def __init__(self, url: str, reason: str = None):
        self.url = url
        self.reason = reason
        # For backward compatibility with tests, don't include reason in the message
        self.message = f"The URL '{url}' is invalid."
        super().__init__(self.message)


async def validate_url(url: str) -> PathValidationResult:
    """
    Checks if a URL is valid

    Args:
        url: The URL to validate

    Returns:
        PathValidationResult indicating if the URL is valid
    """
    if not url:
        return InvalidPathValidationResult(
            error=InvalidUrlError(url=url, reason="URL cannot be empty")
        )

    try:
        result = urlparse(url)
        missing = []
        if not result.scheme:
            missing.append("scheme (e.g., http:// or https://)")
        if not result.netloc:
            missing.append("domain")

        if missing:
            return InvalidPathValidationResult(
                error=InvalidUrlError(
                    url=url, reason=f"Missing required components: {', '.join(missing)}"
                )
            )

        if result.scheme not in ["http", "https"]:
            return InvalidPathValidationResult(
                error=InvalidUrlError(
                    url=url,
                    reason=f"Invalid scheme '{result.scheme}'. Only http and https are supported",
                )
            )

        return ValidPathValidationResult(files=[url])
    except Exception as e:
        return InvalidPathValidationResult(
            error=InvalidUrlError(url=url, reason=f"URL parsing failed: {str(e)}")
        )

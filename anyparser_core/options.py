"""
Options module for Anyparser configuration and parsing.
"""

from dataclasses import dataclass, field
from typing import List, Literal, Optional, TypedDict, Union

from anyparser_core.config.hardcoded import OcrLanguage, OcrPreset

# Type aliases for better readability
AnyparserFormatType = Literal["json", "markdown", "html"]
AnyparserModelType = Literal["text", "ocr", "vlm", "lam", "crawler"]
AnyparserEncodingType = Literal["utf-8", "latin1"]


@dataclass
class AnyparserOption:
    """Configuration options for the Anyparser API."""

    api_url: Optional[str] = None
    api_key: Optional[str] = None
    format: AnyparserFormatType = "json"
    model: AnyparserModelType = "text"
    encoding: AnyparserEncodingType = "utf-8"
    image: Optional[bool] = None
    table: Optional[bool] = None
    files: Optional[Union[str, List[str]]] = None
    ocr_language: Optional[List[OcrLanguage]] = None
    ocr_preset: Optional[OcrPreset] = None
    url: Optional[str] = None
    max_depth: Optional[int] = None
    max_executions: Optional[int] = None
    strategy: Optional[Literal["LIFO", "FIFO"]] = None
    traversal_scope: Optional[Literal["subtree", "domain"]] = None


@dataclass
class UploadedFile:
    """Represents a file that has been prepared for upload."""

    filename: str
    contents: bytes


@dataclass
class AnyparserParsedOption:
    """Validated and processed options ready for API request."""

    api_url: str
    api_key: str
    files: Optional[List[UploadedFile]] = None
    format: AnyparserFormatType = "json"
    model: AnyparserModelType = "text"
    image: Optional[bool] = None
    table: Optional[bool] = None
    ocr_language: Optional[List[OcrLanguage]] = None
    ocr_preset: Optional[OcrPreset] = None
    url: Optional[str] = None
    max_depth: Optional[int] = None
    max_executions: Optional[int] = None
    strategy: Optional[Literal["LIFO", "FIFO"]] = None
    traversal_scope: Optional[Literal["subtree", "domain"]] = None


class DefaultOptions(TypedDict):
    """Default options type definition."""

    api_url: str
    api_key: str
    format: AnyparserFormatType
    model: AnyparserModelType
    image: Optional[bool]
    table: Optional[bool]
    ocr_language: Optional[List[OcrLanguage]]
    ocr_preset: Optional[OcrPreset]
    url: Optional[str]
    max_depth: Optional[int]
    max_executions: Optional[int]
    strategy: Optional[Literal["LIFO", "FIFO"]]
    traversal_scope: Optional[Literal["subtree", "domain"]]


def validate_api_key(api_key: any) -> None:
    """Validate API key format and presence

    Args:
        api_key: API key to validate

    Raises:
        ValueError: If API key is invalid or missing
    """
    if not isinstance(api_key, str):
        raise ValueError("Invalid API key format. API key must be a string.")
    if not api_key:
        raise ValueError(
            "API key is required but not provided. Set ANYPARSER_API_KEY environment variable or pass it in options."
        )


def build_options(options: Optional[AnyparserOption] = None) -> DefaultOptions:
    """Build final options by merging defaults with provided options.

    Args:
        options: User-provided options to override defaults

    Returns:
        Complete options dictionary with all required fields

    Raises:
        ValueError: If required options are missing or invalid
    """
    import os
    from urllib.parse import urlparse

    from .config.hardcoded import FALLBACK_API_URL

    api_url = os.getenv("ANYPARSER_API_URL", FALLBACK_API_URL)
    api_key = os.getenv("ANYPARSER_API_KEY", "")

    # Validate API URL
    try:
        result = urlparse(api_url)
        if not all([result.scheme, result.netloc]):
            raise ValueError
    except ValueError:
        raise ValueError(f"Invalid API URL: {api_url}")

    # Validate API key
    validate_api_key(api_key)

    defaults: DefaultOptions = {
        "api_url": api_url,
        "api_key": api_key,
        "format": "json",
        "model": "text",
        "table": True,
        "image": True,
        "ocr_language": None,
        "ocr_preset": None,
        "url": None,
        "max_depth": None,
        "max_executions": None,
        "strategy": None,
        "traversal_scope": None,
    }

    if options is None:
        return defaults

    # Merge defaults with provided options
    return {**defaults, **vars(options)}

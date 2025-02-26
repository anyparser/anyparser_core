import http.client
import json
import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union, Literal
from urllib.parse import urljoin, urlparse
from datetime import datetime

from .form import build_form
from .options import AnyparserOption
from .request import async_request
from .validator import validate_and_parse
from .version import __version__


@dataclass
class AnyparserImageReference:
    """Represents Anyparser image reference with base64 data, display name, page number, and image index."""

    base64_data: str
    display_name: str
    image_index: int
    page: Optional[int] = None


@dataclass
class AnyparserResultBase:
    """Represents Anyparser base result with rid, original filename, checksum, total characters, and markdown."""

    rid: str
    original_filename: str
    checksum: str
    total_characters: Optional[int] = 0
    markdown: Optional[str] = None


@dataclass
class AnyparserCrawlDirectiveBase:
    """Represents Anyparser crawl directive base with type, priority, name, noindex, nofollow, and crawl delay."""

    type: Literal["HTTP Header", "HTML Meta", "Combined"] = field(default="Combined")
    priority: int = field(default=0)
    name: Optional[str] = field(default=None)
    noindex: Optional[bool] = field(default=False)
    nofollow: Optional[bool] = field(default=False)
    crawl_delay: Optional[int] = field(default=None)
    unavailable_after: Optional[datetime] = field(default=None)


@dataclass
class AnyparserCrawlDirective(AnyparserCrawlDirectiveBase):
    """Represents Anyparser crawl directive with type 'Combined', overriding the name to be None and adding the 'underlying' field."""

    underlying: List[AnyparserCrawlDirectiveBase] = field(default_factory=list)
    type: Literal["Combined"] = field(default="Combined")
    name: Optional[None] = field(default=None)


@dataclass
class AnyparserRobotsTxtDirective:
    """Represents Anyparser robots.txt directive with user agent, disallow, allow, and crawl delay."""

    user_agent: str = field(default="")
    disallow: List[str] = field(default_factory=list)
    allow: List[str] = field(default_factory=list)
    crawl_delay: Optional[int] = field(default=None)


@dataclass
class AnyparserUrl:
    """Represents Anyparser URL with url, title, crawled at, status code, status message, directive, total characters, and markdown."""

    url: str = field(default="")
    status_code: int = field(default=0)
    status_message: str = field(default="")
    politeness_delay: int = field(default=0)
    total_characters: int = field(default=0)
    markdown: str = field(default="")
    directive: AnyparserCrawlDirective = field(default_factory=AnyparserCrawlDirective)
    title: Optional[str] = field(default=None)
    crawled_at: Optional[str] = field(default=None)
    images: List[AnyparserImageReference] = field(default_factory=list)
    text: Optional[str] = field(default=None)


@dataclass
class AnyparserPdfPage:
    """Represents a parsed PDF page with extracted content."""

    page_number: int
    markdown: str
    text: str
    images: List[str]


@dataclass
class AnyparserPdfResult(AnyparserResultBase):
    """Represents a parsed PDF result with extracted content."""

    total_items: int = field(default=0)
    items: List[AnyparserPdfPage] = field(default_factory=list)


@dataclass
class AnyparserCrawlResult:
    """Represents Anyparser crawl result with rid, start url, total characters, total items, markdown, and items."""

    rid: str
    start_url: str
    total_characters: int
    total_items: int
    markdown: str
    items: List[AnyparserUrl]
    robots_directive: AnyparserRobotsTxtDirective


AnyparserResult = Union[AnyparserPdfResult, AnyparserCrawlResult, AnyparserResultBase]


class Anyparser:
    """Main class for parsing itemss using the Anyparser API."""

    def __init__(self, options: Optional[AnyparserOption] = None) -> None:
        """Initialize the parser with optional configuration.

        Args:
            options: Configuration options for the parser
        """
        self.options: Optional[AnyparserOption] = options

    async def parse(
        self, file_paths_or_url: Union[str, List[str]]
    ) -> Union[List[AnyparserResult], str]:
        """Parse files using the Anyparser API.

        Args:
            file_paths_or_url: A single file path or list of file paths to parse, or a start URL for crawling

        Returns:
            List of parsed file results if format is JSON, or raw text content if format is text/markdown

        Raises:
            http.client.HTTPException: If the API request fails
        """

        # Parse and validate the input
        parsed = await validate_and_parse(file_paths_or_url, self.options)

        # Generate a single boundary for the form
        boundary: str = uuid.uuid4().hex

        # Build the form data, passing the boundary
        form_data: bytes = build_form(parsed, boundary)

        # Set up the headers, using the same boundary
        headers: Dict[str, str] = {
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "User-Agent": f"anyparser_core@{__version__}",
        }

        if parsed.api_key:
            headers["Authorization"] = f"Bearer {parsed.api_key}"

        # Parse the URL to extract host and path
        parsed_url = urlparse(str(parsed.api_url))
        host: str = parsed_url.netloc
        path: str = urljoin(str(parsed.api_url), "/parse/v1")

        # Create a connection to the host
        conn = http.client.HTTPSConnection(host)
        try:
            # Make the HTTP request asynchronously
            response = await async_request(conn, "POST", path, form_data, headers)

            # Check if the response is OK
            if response.status != 200:
                text = response.read().decode()
                raise http.client.HTTPException(f"HTTP {response.status}: {text}")

            # Process the response based on the requested format
            # This reads the entire response into memory at once. Avoid uploading too many files or else this could cause OOM errors.
            response_data: bytes = response.read()

            if parsed.format == "json":
                json_data = json.loads(response_data.decode())

                if parsed.model == "crawler":
                    return [
                        AnyparserCrawlResult(
                            rid=item["rid"],
                            start_url=item["start_url"],
                            total_characters=item["total_characters"],
                            total_items=item["total_items"],
                            markdown=item["markdown"],
                            items=[
                                AnyparserUrl(
                                    url=url_item["url"],
                                    status_code=url_item["status_code"],
                                    status_message=url_item["status_message"],
                                    politeness_delay=url_item["politeness_delay"],
                                    total_characters=url_item["total_characters"],
                                    markdown=url_item["markdown"],
                                    directive=AnyparserCrawlDirective(
                                        type=url_item["directive"]["type"],
                                        priority=(
                                            url_item["directive"]["priority"]
                                            if "priority" in url_item["directive"]
                                            else 0
                                        ),
                                        name=(
                                            url_item["directive"]["name"]
                                            if "name" in url_item["directive"]
                                            else None
                                        ),
                                        noindex=(
                                            url_item["directive"]["noindex"]
                                            if "noindex" in url_item["directive"]
                                            else False
                                        ),
                                        nofollow=(
                                            url_item["directive"]["nofollow"]
                                            if "nofollow" in url_item["directive"]
                                            else False
                                        ),
                                        underlying=[
                                            AnyparserCrawlDirectiveBase(**directive)
                                            for directive in url_item["directive"][
                                                "underlying"
                                            ]
                                            if "underlying" in url_item["directive"]
                                        ],
                                    ),
                                    title=url_item["title"],
                                    crawled_at=url_item["crawled_at"],
                                )
                                for url_item in item["items"]
                                if url_item["url"] is not None
                            ],
                            robots_directive=AnyparserRobotsTxtDirective(
                                user_agent=(
                                    item["robots_directive"]["user_agent"]
                                    if "user_agent" in item["robots_directive"]
                                    else ""
                                ),
                                allow=(
                                    item["robots_directive"]["allow"]
                                    if "allow" in item["robots_directive"]
                                    else []
                                ),
                                disallow=(
                                    item["robots_directive"]["disallow"]
                                    if "disallow" in item["robots_directive"]
                                    else []
                                ),
                                crawl_delay=(
                                    item["robots_directive"]["crawl_delay"]
                                    if "crawl_delay" in item["robots_directive"]
                                    else 0
                                ),
                            ),
                        )
                        for item in json_data
                    ]

                return [
                    (
                        AnyparserPdfResult(
                            **{
                                **{k: v for k, v in item.items() if k != "items"},
                                "items": [
                                    AnyparserPdfPage(**page)
                                    for page in item.get("items", [])
                                ],
                            }
                        )
                        if item["original_filename"].endswith(".pdf")
                        else AnyparserResultBase(**item)
                    )
                    for item in json_data
                ]

            return response_data.decode()
        finally:
            conn.close()

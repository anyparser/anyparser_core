"""
Form data builder module for creating multipart form data for API requests.
"""

import mimetypes
from typing import Any

from .options import AnyparserParsedOption


def build_form(parsed: AnyparserParsedOption, boundary: str) -> bytes:
    """
    Builds multipart form data from parsed options.

    Args:
        parsed: Validated parser options
        boundary: The boundary string to use for the form

    Returns:
        The form data as a byte string for use in an HTTP request
    """
    form_data: bytearray = bytearray()
    crlf: bytes = b"\r\n"

    # Helper function to add a field to the form
    def add_field(name: str, value: Any) -> None:
        """Add a field to the form data.

        Args:
            name: Field name
            value: Field value
        """
        form_data.extend(f"--{boundary}".encode("utf-8"))
        form_data.extend(crlf)
        form_data.extend(
            f'Content-Disposition: form-data; name="{name}"'.encode("utf-8")
        )
        form_data.extend(crlf)
        form_data.extend(crlf)
        form_data.extend(str(value).encode("utf-8"))
        form_data.extend(crlf)

    # Add regular form fields
    add_field("format", parsed.format)
    add_field("model", parsed.model)

    # Only add image and table fields if not using OCR model or crawler model
    if parsed.model != "ocr" and parsed.model != "crawler":
        if parsed.image is not None:
            add_field("image", str(parsed.image))
        if parsed.table is not None:
            add_field("table", str(parsed.table))

    if parsed.model == "ocr":
        if parsed.ocr_language:
            add_field(
                "ocr_language", ",".join([lang.value for lang in parsed.ocr_language])
            )

        if parsed.ocr_preset:
            add_field("ocr_preset", parsed.ocr_preset.value)

    if parsed.model == "crawler":
        add_field("url", parsed.url)
        add_field("max_depth", parsed.max_depth)
        add_field("max_executions", parsed.max_executions)
        add_field("strategy", parsed.strategy)
        add_field("traversal_scope", parsed.traversal_scope)
    else:
        # Add files to the form
        for file in parsed.files:
            file_content: bytes = file.contents
            file_name: str = file.filename

            # Guess the MIME type
            content_type: str = (
                mimetypes.guess_type(file_name)[0] or "application/octet-stream"
            )

            form_data.extend(f"--{boundary}".encode("utf-8"))
            form_data.extend(crlf)
            form_data.extend(
                f'Content-Disposition: form-data; name="files"; filename="{file_name}"'.encode(
                    "utf-8"
                )
            )
            form_data.extend(crlf)
            form_data.extend(f"Content-Type: {content_type}".encode("utf-8"))
            form_data.extend(crlf)
            form_data.extend(crlf)
            form_data.extend(file_content)
            form_data.extend(crlf)

    # Add the final boundary
    form_data.extend(f"--{boundary}--".encode("utf-8"))
    form_data.extend(crlf)

    return bytes(form_data)

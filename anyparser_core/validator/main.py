"""
Option validation and parsing module
"""

import fcntl
import os
from contextlib import contextmanager
from pathlib import Path
from typing import Generator, List, Union

from anyparser_core.options import AnyparserOption, UploadedFile
from anyparser_core.validator.url import validate_url

from ..options import AnyparserParsedOption, build_options
from .option import validate_option
from .path import validate_path


@contextmanager
def file_lock(file_path: Union[str, Path]) -> Generator:
    """Context manager for file locking to prevent race conditions.

    Args:
        file_path: Path to the file to lock

    Yields:
        File object with exclusive lock

    Raises:
        IOError: If file is locked by another process
        FileNotFoundError: If file does not exist
    """
    if isinstance(file_path, Path):
        file_path = str(file_path)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} does not exist")

    with open(file_path, "rb") as f:
        try:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            yield f
        except BlockingIOError:
            raise IOError(f"File {file_path} is locked by another process")
        finally:
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)


async def validate_and_parse(
    file_paths: Union[str, List[str]], options: Union[AnyparserOption, None] = None
) -> AnyparserParsedOption:
    """
    Validates options and processes input files

    Args:
        file_paths: Files to process
        options: Parser options

    Returns:
        Processed options and files
    """

    parsed = build_options(options)
    validate_option(parsed)

    result = (
        await validate_url(file_paths)
        if options is not None and options.model == "crawler"
        else await validate_path(file_paths)
    )

    if not result.valid:
        raise result.error

    parsedOption = AnyparserParsedOption(
        api_url=parsed["api_url"],
        api_key=parsed["api_key"],
        format=parsed.get("format", "json"),
        model=parsed.get("model", "text"),
        image=parsed.get("image", True),
        table=parsed.get("table", True),
        ocr_language=parsed.get("ocr_language"),
        ocr_preset=parsed.get("ocr_preset"),
        url=parsed.get("url"),
        max_depth=parsed.get("max_depth"),
        max_executions=parsed.get("max_executions"),
        strategy=parsed.get("strategy"),
        traversal_scope=parsed.get("traversal_scope"),
    )

    processed = []

    if options is not None and options.model == "crawler":
        url = result.files[0]
        parsedOption.url = url
    else:
        for file_path in result.files:
            path = Path(file_path)
            try:
                with file_lock(path) as f:
                    contents = f.read()
                    processed.append(
                        UploadedFile(filename=path.name, contents=contents)
                    )
            except BlockingIOError:
                raise IOError(f"File {path} is locked by another process")
            except FileNotFoundError:
                raise FileNotFoundError(f"File {path} was not found or was removed")

        parsedOption.files = processed

    return parsedOption

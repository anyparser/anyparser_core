"""
Validation module for file paths
"""

from pathlib import Path
from typing import List, Union

from .validation import (
    InvalidPathValidationResult,
    PathValidationResult,
    ValidPathValidationResult,
)


async def validate_path(file_paths: Union[str, List[str]]) -> PathValidationResult:
    """
    Validates file paths exist and are accessible
    """
    if not file_paths or (isinstance(file_paths, str) and not file_paths.strip()):
        return InvalidPathValidationResult(error=FileNotFoundError("No files provided"))

    if isinstance(file_paths, (str, Path)):
        files = [file_paths]
    else:
        files = file_paths

    for file_path in files:
        path = Path(file_path)
        if not path.exists():
            return InvalidPathValidationResult(
                error=FileNotFoundError(f"File does not exist: {file_path}")
            )

    return ValidPathValidationResult(files=files)

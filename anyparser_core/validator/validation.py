"""
Type definitions for validation results in the anyparser_core package.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Union


@dataclass
class ValidPathValidationResult:
    """Result for successful path validation."""

    valid: bool = True
    files: List[str] = field(default_factory=list)


@dataclass
class InvalidPathValidationResult:
    """Result for failed path validation."""

    valid: bool = False
    error: Optional[Exception] = None


# Type alias for path validation results
PathValidationResult = Union[ValidPathValidationResult, InvalidPathValidationResult]

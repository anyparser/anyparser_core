from .config.hardcoded import OcrLanguage, OcrPreset
from .form import build_form
from .options import AnyparserOption, AnyparserParsedOption, UploadedFile
from .parser import (
    Anyparser,
    AnyparserCrawlDirective,
    AnyparserCrawlDirectiveBase,
    AnyparserCrawlResult,
    AnyparserImageReference,
    AnyparserPdfPage,
    AnyparserPdfResult,
    AnyparserResult,
    AnyparserResultBase,
    AnyparserRobotsTxtDirective,
    AnyparserUrl,
)
from .validator import validate_and_parse, validate_option, validate_path
from .version import __version__

__all__ = [
    "Anyparser",
    "AnyparserCrawlDirective",
    "AnyparserCrawlDirectiveBase",
    "AnyparserCrawlResult",
    "AnyparserImageReference",
    "AnyparserPdfPage",
    "AnyparserPdfResult",
    AnyparserResult,
    "AnyparserResultBase",
    "AnyparserRobotsTxtDirective",
    "AnyparserUrl",
    "validate_and_parse",
    "validate_and_parse",
    "validate_path",
    "validate_option",
    "build_form",
    "Anyparser",
    "OcrPreset",
    "OcrLanguage",
]
